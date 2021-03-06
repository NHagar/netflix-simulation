import numpy as np
import pandas as pd
from scipy.spatial.distance import jensenshannon
from scipy.stats import kstest

def compare_ranks(r, rank_col):
    if r['next_rank'] != r['next_rank']:
        return 'exit'

    if r['next_rank'] > r[rank_col]:
        return 'decrease'
    elif r['next_rank'] == r[rank_col]:
        return 'same'
    else:
        return 'increase'

def time_on_list(data: pd.DataFrame, 
                 item_col: str, 
                 iter_col: str) -> pd.DataFrame:
    """generates distribution of how long items 
       spend on top 10 list"""
    ""
    weeks_per_item = data.groupby(item_col).nunique()[iter_col].reset_index().groupby(iter_col).count()

    return weeks_per_item

def churn(data: pd.DataFrame,
          item_col: str,
          iter_col: str) -> list[int]:
    """generates distribution of WoW churn"""
    weeks = data.sort_values(by=iter_col)[iter_col].drop_duplicates().tolist()
    weeks_pairs = list(zip(weeks, weeks[1:]))
    churn = []
    for w in weeks_pairs:
        turnover = len(set(data[data[iter_col]==w[0]][item_col]) - set(data[data[iter_col]==w[1]][item_col]))
        churn.append(turnover)

    return churn

def movement_prob(data: pd.DataFrame,
                  item_col: str,
                  iter_col: str,
                  rank_col: str):
    """generates distribution of movement probabilities
       over ranks"""
    sample = data.sort_values(by=[item_col, iter_col])[[item_col, rank_col, iter_col]]
    sample['next_rank'] = sample.groupby(item_col)[rank_col].shift(-1)
    sample['transition'] = sample.apply(compare_ranks, rank_col=rank_col, axis=1)
    counts = (sample.groupby([rank_col, 'transition']).count()[iter_col].reset_index()\
        .pivot_table(index=rank_col, columns='transition', values=iter_col)\
        .fillna(0))

    pcts = counts.apply(lambda x: x / x.sum(), axis=1)

    return pcts

def compare_distributions(dist_1, dist_2):
    """generates fit measure for distribution"""
    if type(dist_1) == list:
        return kstest(np.array(dist_1), np.array(dist_2))
    elif "decrease" in dist_1.columns:
        results = []
        for i in range(1, 11):
            emp = dist_1.loc[i]
            sim = dist_2.loc[i]
            js = jensenshannon(emp, sim)
            results.append(js)
        return sum(results) / len(results)
    else:
        joined = dist_1.join(dist_2, how='outer').fillna(0)
        return kstest(joined.values[:,0], joined.values[:,1])