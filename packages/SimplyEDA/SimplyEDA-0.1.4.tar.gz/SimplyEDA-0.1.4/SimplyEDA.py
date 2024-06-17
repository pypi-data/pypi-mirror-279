#!/usr/bin/env python
# coding: utf-8

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def remove_outlier(col, multiplier=1.5):
    """
    Remove outliers from a column based on the Interquartile Range (IQR) method.

    Parameters:
    col (pd.Series): The column from which to remove outliers.
    multiplier (float): The multiplier for the IQR to define outliers. Default is 1.5.

    Returns:
    tuple: Lower and upper range for outlier detection.
    """
    Q1, Q3 = np.percentile(col, [25, 75])
    IQR = Q3 - Q1
    lower_range = Q1 - (multiplier * IQR)
    upper_range = Q3 + (multiplier * IQR)
    return lower_range, upper_range

def find_specialchar(df):
    """
    Find special characters in a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to check.

    Returns:
    None
    """
    for feature in df.columns:
        print(f'The unique values in {feature} are as below:')
        print(df[feature].unique())
        print('\n')

def vif_cal(input_data):
    """
    Calculate Variance Inflation Factor (VIF) for each feature in the DataFrame.

    Parameters:
    input_data (pd.DataFrame): The DataFrame for which to calculate VIF.

    Returns:
    None
    """
    from statsmodels.stats.outliers_influence import variance_inflation_factor

    x_vars = input_data
    xvar_names = input_data.columns
    for i in range(0, xvar_names.shape[0]):
        vif = variance_inflation_factor(x_vars.values, i)
        print(f"{xvar_names[i]} VIF = {vif:.2f}")

def dups(df):
    """
    Show duplicate summary of a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to check for duplicates.

    Returns:
    None
    """
    dps = df.duplicated()
    print(f'Number of duplicate rows = {dps.sum()}')
    print(df.shape)

def boxplt_continous(df):
    """
    Plot boxplots for all continuous features in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to plot.

    Returns:
    None
    """
    for feature in df.columns:
        if df[feature].dtype != 'object':
            sns.boxplot(df[feature], whis=1.5)
            plt.grid()
            plt.show()
