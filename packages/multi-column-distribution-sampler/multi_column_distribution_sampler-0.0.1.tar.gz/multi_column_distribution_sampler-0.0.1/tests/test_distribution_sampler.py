import pytest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'multi_column_distribution_sampler'))
from multi_column_distribution_sampler import get_weighted_sample
# the test dataset is taken from UCI Machine Learning Repo
from ucimlrepo import fetch_ucirepo 

# fetch dataset 
car_evaluation = fetch_ucirepo(id=19) 
# get the dataset as a dataframe
car_evaluation_df = car_evaluation.data.original

# create list of columns taken for weighted sampling
cols_list = ['buying', 'maint', 'doors', 'persons']

@pytest.mark.parametrize('i', [1,2,3,4])
@pytest.mark.parametrize('sample_size', [1,10,100,500,1000,1728])
def test_get_weighted_sample(i, sample_size):
    
    # get distribution for the combination of columns
    cols_combination = cols_list[:i]
    cols_combination_dist = car_evaluation_df.groupby(cols_combination).size().reset_index(name='count')
    # normalize the counts
    cols_combination_dist['count'] = cols_combination_dist['count'].div(cols_combination_dist['count'].sum()).round(2)
    # get sample using the function
    sampled_df = get_weighted_sample(car_evaluation_df, cols_combination, sample_size)
    sampled_df_dist = sampled_df.groupby(cols_combination).size().reset_index(name='count')
    sampled_df_dist['count'] = sampled_df_dist['count'].div(sampled_df_dist['count'].sum()).round(2)

    cols_combination_dist.sort_values(by=cols_combination, inplace=True)
    sampled_df_dist.sort_values(by=cols_combination, inplace=True)

    # check if all valid combinations of categories are included in the sample, and
    # check if the category combinations are properly sampled
    col_values_combinations = [' '.join(combinations) for combinations in cols_combination_dist[cols_combination].apply(tuple, axis=1)]
    col_values_combinations_sample = [' '.join(combinations) for combinations in sampled_df_dist[cols_combination].apply(tuple, axis=1)]

    for i, values_combination in enumerate(col_values_combinations):
        assert values_combination in col_values_combinations_sample, f'{" ".join(values_combination)} combination of column values is not included in sampled dataframe'

        assert abs(cols_combination_dist.iloc[i]['count'] - sampled_df_dist.iloc[i]['count']) < 0.5, f'{" ".join(values_combination)} not sampled properly'