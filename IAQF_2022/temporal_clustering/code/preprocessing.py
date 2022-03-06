import pandas as pd
import numpy as np
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
from tslearn.clustering import TimeSeriesKMeans

import statsmodels
from statsmodels.tsa.stattools import adfuller


def first_valid_table(dataframe):
    """
    get first valid information for the given data
    :param dataframe: pd.DataFrame;
    :return:
    """
    first_valid = pd.DataFrame(columns=['first_valid_date', 'total_N/A', 'N/A_since_first_valid'])
    # first obs date
    first_valid['first_valid_date'] = dataframe.apply(lambda x: x.first_valid_index())
    # Total NA
    first_valid['total_N/A'] = dataframe.apply(lambda x: x.isnull().sum(axis=0))
    # NA since first_date
    first_valid['N/A_since_first_valid'] = dataframe.apply(lambda x: x.loc[x.first_valid_index():].isnull().sum(axis=0))

    first_valid.sort_values("first_valid_date", inplace=True)
    return first_valid


def adf_table(series):
    """
    run adf test for initial time series from first valid
    Fixed-width Fractional Difference (FFD)
    article source: https://www.kaggle.com/elvisesp/time-series-analysis-using-fractional-differencing
    code source: https://gist.github.com/skuttruf/fb82807ab0400fba51c344313eb43466
    :param series: pd.DataFrame;
    :return:
    """
    # adf = pd.DataFrame(columns=['ADF Statistic', 'ADF p-value', 'Reject H0 at 5%?'])
    # first obs date
    series = series.loc[series.first_valid_index():]
    adf_test = adfuller(series)
    reject = "Yes" if adf_test[1] < 0.05 else "No"
    return round(adf_test[0], 4), round(adf_test[1], 4), reject


def get_weights(d, lags):
    """
    # code for partial differentiation
    # get the weights of past data for each data point
    :param d:
    :param lags:
    :return: weights from the series expansion of the differencing operator
    """
    # for real orders d and up to lags coefficients
    w = [1]
    for k in range(1, lags):
        w.append(-w[-1] * (d - k + 1) / k)
    w = np.array(w).reshape(-1, 1)
    return w


def cutoff_find(order, cutoff, start_lags):
    """

    :param order: int; order is our dearest d, cutoff is 1e-5 for us,
    :param cutoff:
    :param start_lags: int; an initial amount of lags in which the loop will start
    :return:
    """
    # this can be set to high values in order to speed up the algo.
    val = np.inf
    lags = start_lags
    while abs(val) > cutoff:
        w = get_weights(order, lags)
        val = w[len(w) - 1]
        lags += 1
    return lags


def ts_differencing_tau(series, order, tau):
    """

    :param series:
    :param order:
    :param tau:
    :return: return the time series resulting from (fractional) differencing
    """
    lag_cutoff = (cutoff_find(order, tau, 1))  # finding lag cutoff with tau
    weights = get_weights(order, lag_cutoff)
    res = 0
    for k in range(lag_cutoff):
        res += weights[k] * series.shift(k).fillna(0)
    return res[lag_cutoff:]


def df_differencing_table(series, possible_order, tau):
    """
    used for calculating best fractionally differenced data on series level
    remove VIX from training since it is already stationary
    :param series: pd.Series; given feature series
    :param possible_order: np.array; range of possible fractional difference order
    :param tau:
    :return:
    """
    for i in tqdm(range(len(possible_order)), postfix="order_picking"):
        diff_series = ts_differencing_tau(series.loc[series.first_valid_index():], possible_order[i], tau)
        p_value = adfuller(diff_series)[1]
        if p_value <= 0.05:
            return diff_series


def df_differencing_order(series, possible_order, tau):
    """

    :param series:
    :param possible_order:
    :param tau:
    :return:
    """
    for i in tqdm(range(len(possible_order)), postfix="order_picking"):
        diff_series = ts_differencing_tau(series.loc[series.first_valid_index():], possible_order[i], tau)
        p_value = adfuller(diff_series)[1]
        if p_value <= 0.05:
            return possible_order[i]


def diff_origin_corr(feature_name, orig_df, diff_df):
    """
    correlation with original series table, ffd one and first order one
    :param feature_name: list; contains names of selected index
    :param orig_df: pd.DataFrame; undifferenced data
    :param diff_df: pd.DataFrame; fractionally differenced data
    :return: pd.DataFrame; correlation table
    """
    corr_tab = pd.DataFrame(columns=['ffd correlation', 'd=1 correlation'])
    for col in feature_name:
        corr_frc = orig_df[col].corr(diff_df[col])
        corr_fst = orig_df[col].diff().corr(orig_df[col])
        corr_tab.loc[col] = corr_frc, corr_fst
    return corr_tab


def main():
    df = pd.read_csv(r".\data\newData_Feb11.csv").set_index('Date')

    # since we only care about trading until the end of 2021, we drop all data after that
    df = df.loc[: '2022-01-01']

    # check nan info
    fst_valid = first_valid_table(df)

    # forward filling
    df = df.fillna(method='ffill')

    # check difference info
    diff_info_pre = df.apply(lambda x: adf_table(x))
    diff_info_pre.index = ['ADF Statistic', 'ADF p-value', 'Reject H0 at 5%?']
    diff_info_pre = diff_info_pre.T
    diff_info_pre.to_csv(r".\data\adf_table_before_difference.csv")

    # train difference level
    possible_d = np.divide(range(1, 100), 100)
    tqdm.pandas(desc="calculation")
    difference_order = df.progress_apply(lambda y: df_differencing_order(y, possible_d, 1e-4))
    difference_table = df.progress_apply(lambda y: df_differencing_table(y, possible_d, 1e-4))
    difference_table.to_csv(r".\data\fractionally_differenced_data.csv")

    diff_info_pro = difference_table.apply(lambda x: adf_table(x))
    diff_info_pro.index = ['ADF Statistic', 'ADF p-value', 'Reject H0 at 5%?']
    diff_info_pro = diff_info_pro.T
    diff_info_pro['differentiation degree (d)'] = difference_order
    diff_info_pro.to_csv(r".\data\adf_table_after_difference.csv")

    # correlation table
    features = df.columns
    correlation_table = diff_origin_corr(features, df, difference_table)
    correlation_table.to_csv(r".\data\correlation_table.csv")


if __name__ == "__main__":
    main()



