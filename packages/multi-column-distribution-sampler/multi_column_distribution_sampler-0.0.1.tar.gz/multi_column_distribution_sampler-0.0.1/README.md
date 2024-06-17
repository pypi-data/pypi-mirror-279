# MULTI COLUMN DISTRIBUTION SAMPLER

Function to draw a sample from a given dataframe while maintaining the same distribution of the columns of interest.
Also includes a function to determine the minimum sample size needed to ensure the distribution of the columns of interest in the given dataframe.

## Overview

In order to draw a sample from a `pandas dataframe` we can use the `sample` function. But, this doesn't ensure that the sample drawn would be representative of the distributions of the columns of interest in the dataframe. Although we can use the `train_test_split` with `stratify` from `sklearn.model_selection` for stratified sampling, things get complex once we want the sample to follow the exact distribution for multiple columns. This package abstracts away all the logic and provides you with functions that can be used to determine the minimum sample size reqired for a distributive sample and also the sample itself when involving multiple columns. Since this package ensures a perfect representative sample, the resulting sample will probably be a bit larger compared to the sample size desired. This increase in sample size will be depending on the distributions of the columns in the actual dataframe and also the number of columns factored in while sampling.

## Features

* Multi column based representative sampling
* Handles both continuous and categorical features
* Uses Gini index to measure impurity of partion
* Includes basic tree printing functionality for tree visualization

# Requirements

Python 3.x
[Optional] Any text editor or IDE of your choice for editing the code.

# Installation

multi_column_distribution_sampler can be installed using the following command:

```
pip install multi_column_distribution_sampler
```
or
```
pip3 install multi_column_distribution_sampler
```

# Dependencies

multi_column_distribution_sampler depends on the following packages:-

* numpy
* pandas

## License

MIT License