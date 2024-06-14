import torch
from thoi.measures.gaussian_copula import nplets_measures


def _evaluate_nplet(covmat: torch.tensor, T:int, batched_nplets: torch.tensor, metric:str):

    """
        X (torch.tensor): The covariance matrix with shape (n_variables, n_variables)
        batched_nplets (torch.tensor): The nplets to calculate the inverse of the oinformation with shape (batch_size, order)
        metric (str): The metric to evaluate. One of tc, dtc, o or s
    """

    # get the metric index to get from the result of nplets
    METRICS = ['tc', 'dtc', 'o', 's']
    metric_idx = METRICS.index(metric)

    # |batch_size| x |4 = (tc, dtc, o, s)|
    batched_res = nplets_measures(covmat, batched_nplets, T=T, covmat_precomputed=True)

    # Return minus the o information score to make it an maximum optimization (energy)
    # |batch_size|
    res = batched_res[:,metric_idx].flatten()

    return res