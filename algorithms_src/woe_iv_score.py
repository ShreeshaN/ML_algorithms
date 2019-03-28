# -*- coding: utf-8 -*-
"""
@created on: 27/03/19,
@author: Shreesha N,
@version: v0.0.1

Description:

Sphinx Documentation Status:

..todo::

"""

import numpy as np
import pandas as pd
import traceback

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)


def encode_continuous_column(data_column, category_count=10):
    """
    Converts a continuous column into categorical based on category_count value
    :param data_column: structure containing continuous data
    :param category_count: number of buckets to create
    :return: encoded column from continuous column to categorical column
    """
    encoded_column = pd.cut(data_column, category_count, labels=['cat_' + str(x) for x in range(category_count)])
    return encoded_column


def calculate_woe(data, independent_var, dependent_var, is_continuous=None, category_count=10):
    """
    Calculates weight of evidence of a independent variable against a dependent variable
    :param data: dataframe which contains feature a
    :param independent_var: variable whose woe needs to be calculated
    :param dependent_var: target variable
    :param is_continuous: Default None; Boolean indicating whether the independent_var passed in categorical or continuous
    :param category_count: Default 10; If the independent variable is continuous, this parameter defines the number of categories to derive from the variable
    :return: dictionary containing woe and iv scores under key 'woe' and 'iv 'of the independent variable
    """
    # calculate total number of positive and negative samples in data
    total_bads = data[dependent_var].sum()
    total_goods = len(data) - total_bads
    if total_bads == 0 or total_goods == 0:
        raise Exception('Target variable does not contain two classes. ')

    # check if column is continuous, if yes convert it to bucketize
    if is_continuous:
        data[independent_var] = encode_continuous_column(data[independent_var], category_count=category_count)
    elif data[independent_var].dtype == np.float:
        data[independent_var] = encode_continuous_column(data[independent_var], category_count=category_count)

    # pivot on independent variable to get counts of goods and bads
    pivot = pd.pivot_table(data, index=independent_var, columns=dependent_var, aggfunc='count')
    feature_uniques = data[independent_var].unique()

    # dictionary to hold values required for iv calculation
    values = {'category': [], 'goods_count': [], 'bads_count': [], 'goods_percentage': [], 'bads_percentage': [],
              'woe': [], 'iv': []}

    # iterate over all the unique categories in the independent variable
    for f in feature_uniques:
        values['category'].append(f)

        goods_count = pivot.loc[f][0]
        values['goods_count'].append(goods_count)

        bads_count = pivot.loc[f][1]
        values['bads_count'].append(bads_count)

        goods_percentage = goods_count / total_goods
        values['goods_percentage'].append(goods_percentage)

        bads_percentage = bads_count / total_bads
        values['bads_percentage'].append(bads_percentage)

        woe = np.log(goods_percentage / bads_percentage)
        values['woe'].append(woe)

        iv = (woe * (goods_percentage - bads_percentage))
        values['iv'].append(iv)
    return values


def calculate_iv(data, independent_var, dependent_var, is_continuous=None, category_count=10):
    """
    This function assumes the data passed is treated for null values and any other irregularities
    Calculates information value of a independent variable against a dependent variable
    :param data: dataframe which contains feature a
    :param independent_var: variable whose IV needs to be calculated
    :param dependent_var: target variable
    :param is_continuous: Default None; Boolean indicating whether the independent_var passed in categorical or continuous
    :param category_count: Default 10; If the independent variable is continuous, this parameter defines the number of categories to derive from the variable
    :return: iv score of the independent variable
    """
    try:
        values = calculate_woe(data, independent_var, dependent_var, is_continuous, category_count)
        df = pd.DataFrame(values)
        return df['iv'].sum()
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    iv_scores = {}
    csv_filepath = ''
    data = pd.read_csv(csv_filepath)
    data = data.fillna(0)
    target_column = 'Actual Label'
    id_column = 'Customer_ID'
    cols_to_calculate_iv = [x for x in data.columns if x not in [target_column, id_column]]
    for col in cols_to_calculate_iv:
        print(col)
        iv_score = calculate_iv(data, col, target_column)
        iv_scores[col] = iv_score
    print(iv_scores)
