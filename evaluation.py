import pandas as pd

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



    return distribution

def movement_prob(data):
    """generates distribution of movement probabilities
       over ranks"""

    return distribution

def compare_distributions(dist_1, dist_2):
    """generates fit measure for distribution"""

    return fit