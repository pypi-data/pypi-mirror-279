import torch
import numpy as np
from torch.optim import LBFGS
import gc
from natsort import natsorted
import pandas as pd

def closure(G, P, L, optimizer, lambda_l2, losses):
    def closure_fn():
        optimizer.zero_grad()
        predictions1 = torch.matmul(L, P)
        predictions2 = torch.matmul(L.T, G)
        criterion = torch.nn.MSELoss()
        loss = criterion(predictions1, G) + criterion(predictions2, P) + lambda_l2 * torch.norm(L, 2)
        losses.append(loss.item())
        loss.backward()
        torch.cuda.empty_cache()
        gc.collect()
        return loss

    return closure_fn


def linkage(rna_adata, atac_adata, meta, min_cell=10, lr=0.5, max_iter=500, lambda_l2=0.1):
    chrs = natsorted([element for element in np.unique(meta[3].tolist()) if element.startswith('chr')])
    linkage = []
    losses_list = []
    for chr in chrs:
        print(chr)
        chr_p = chr + '-'
        chr_gene = np.unique(
            meta.iloc[np.where((meta[3].to_numpy() == chr) & (meta[2].to_numpy() == 'Gene Expression'))][1].to_numpy())
        chr_peak = [peak.replace(':', '-') for peak in [item for item in atac_adata.var.index if chr_p in item]]
        chr_gene = np.sort(np.array(list(set(chr_gene).intersection(set(rna_adata.var.index)))))
        chr_peak = np.sort(np.array(list(set(chr_peak).intersection(set(atac_adata.var.index)))))

        gene_to_index = {gene: idx for idx, gene in enumerate(rna_adata.var.index)}
        gene_indices = [gene_to_index[gene] for gene in chr_gene if gene in gene_to_index]
        chr_gene_exp_data = rna_adata.X[:, gene_indices].T.toarray()

        peak_to_index = {peak: idx for idx, peak in enumerate(atac_adata.var.index)}
        peak_indices = [peak_to_index[peak] for peak in chr_peak if peak in peak_to_index]
        chr_peak_exp_data = atac_adata.X[:, peak_indices].T.toarray()

        select_gene = chr_gene[np.where(np.sum(chr_gene_exp_data > 0, axis=1) > min_cell)[0]]
        select_peak = chr_peak[np.where(np.sum(chr_peak_exp_data > 0, axis=1) > min_cell)[0]]

        select_gene_to_index = {gene: idx for idx, gene in enumerate(chr_gene)}
        select_gene_indices = [select_gene_to_index[gene] for gene in select_gene if gene in gene_to_index]
        chr_gene_exp_data = chr_gene_exp_data[select_gene_indices, :]

        select_peak_to_index = {peak: idx for idx, peak in enumerate(chr_peak)}
        select_peak_indices = [select_peak_to_index[peak] for peak in select_peak if peak in peak_to_index]
        chr_peak_exp_data = chr_peak_exp_data[select_peak_indices, :]

        G = torch.from_numpy(chr_gene_exp_data).cuda(0)
        P = torch.from_numpy(chr_peak_exp_data).cuda(0)
        G = (G - torch.mean(G, dim=0)) / torch.std(G, dim=0)
        P = (P - torch.mean(P, dim=0)) / torch.std(P, dim=0)
        L = torch.rand((G.shape[0], P.shape[0]), requires_grad=True, device="cuda")
        losses = []
        optimizer = LBFGS([L], lr=lr, max_iter=max_iter, tolerance_grad=1e-07)
        closure_fn = closure(G, P, L, optimizer, lambda_l2, losses)
        optimizer.step(closure_fn)
        losses_list.append(losses)
        result = pd.DataFrame(L.cpu().detach().numpy(), index=select_gene, columns=select_peak)
        linkage.append(result)
        torch.cuda.empty_cache()
        gc.collect()

    return linkage