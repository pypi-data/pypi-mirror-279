import pandas as pd
import math

def _get_sample_size_for_group(weights: pd.Series, group: str, total_sample_size: int, max_group_sample_size: int) -> int:
    """Function to get the sample size for a given category/group
    of the given column.
    
    Parameters
    ----------
    weights: Series
        A pandas series where the index is categories/groups within
        a given column and the values are the correponding counts.
    group: str
        A particular category/group within the column.
    total_sample_size: int
        Size of the sample to be taken.
    max_group_sample_size: int
        Maximum allowed size for the sample forming the category/group of the column.

    Returns
    -------
    int
        Sample size for the category/group.
    """
    try:
        group_sample_size = math.ceil(weights[group] * total_sample_size)
        if group_sample_size > max_group_sample_size:
            group_sample_size = max_group_sample_size
        return group_sample_size
    except:
        return 0

def _get_weighted_sample(df: pd.DataFrame, columns: list[str], total_sample_size: int, random_state: int=42) -> pd.DataFrame:
    """Recursive function to sample from a given dataframe while maintaining
    the same distribution of the column of interest
    
    Parameters
    ----------
    df: DataFrame
        The dataframe to be sampled.
    columns: list[str]
        List of column names. These are the columns whose distributions are used for the sampling.
        In each call of this function, the first column in the list will be used 
    total_sample_size: int
        Size of the sample to be taken.
    randon_state: int, default = 42
        Use random state for reproducible results

    Returns
    -------
    DataFrame
        
    """
    category_weights = df[columns[0]].value_counts(normalize=True)

    def sample_group(group: pd.DataFrame):
        group_sample_size = _get_sample_size_for_group(category_weights, group.name, total_sample_size, len(group))
        if len(columns[1:]) < 1:
            return group.sample(n=group_sample_size, random_state=random_state)
        else:
            return _get_weighted_sample(group, columns[1:], group_sample_size, random_state=random_state)

    return df.groupby(columns[0], group_keys=False).apply(sample_group, include_groups=False)

def get_weighted_sample(df: pd.DataFrame, columns: list[str], total_sample_size: int, random_state: int=42):
    """Function to sample from a given dataframe while maintaining
    the same distribution of the columns of interest
    
    Parameters
    ----------
    df: DataFrame
        The dataframe to be sampled.
    columns: list[str]
        List of column names. These are the columns whose distributions are used for the sampling.
    total_sample_size: int
        Size of the sample to be taken.
    randon_state: int, default = 42
        Use random state for reproducible results

    Returns
    -------
    DataFrame
        Sampled dataframe.
    """

    # add unique id column:
    # this is because the groupby operation when recuresed with multiple columns will result in the loss of some of the columns grouped.
    # a unique id is added so that after sampling, the sampled ids can be used to retrieve the full data from the dataframe before sampling.
    df['_sample_unique_id_'] = range(len(df))
    # create a copy of the input dataframe and use if for the sampling operation, so as not to modify the input dataframe
    sampled_df = df.copy()
    # get sample
    sampled_df = _get_weighted_sample(sampled_df, columns, total_sample_size, random_state)
    # merge with the input dataframe to get all features
    sampled_df = pd.merge(df, sampled_df[['_sample_unique_id_']], how='inner', on='_sample_unique_id_')
    # remove the unique identifier used
    df.drop(columns='_sample_unique_id_', inplace=True)
    sampled_df.drop(columns='_sample_unique_id_', inplace=True)

    return sampled_df

def get_min_distribution_sample_size(df: pd.DataFrame, columns: list[str], random_state: int=42):
    """Function to determine the minimum sample size needed to form a representative sample from
    a given dataframe maintaining the same distribution of the columns of interest
    
    Parameters
    ----------
    df: DataFrame
        The dataframe to be sampled.
    columns: list[str]
        List of column names. These are the columns whose distributions are used for the sampling.
    randon_state: int, default = 42
        Use random state for reproducible results

    Returns
    -------
    int
        Minimum sample size.
    """

    sampled_df = get_weighted_sample(df, columns, 1, random_state)

    return sampled_df.shape[0]