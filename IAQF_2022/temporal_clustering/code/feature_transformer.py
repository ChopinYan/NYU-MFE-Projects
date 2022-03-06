import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from tslearn.clustering import TimeSeriesKMeans
from tslearn.clustering import silhouette_score
# from sklearn.model_selection import GridSearchCV
# from sklearn.cluster import DBSCAN
# import statsmodels
# from statsmodels.tsa.stattools import adfuller
# import time
import math

# from dtw_calculation import DTW


def sliding_window(feature_series, win, step=1):
    """

    :param feature_series:
    :param win:
    :param step:
    :return:
    """

    # feature series start from the first valid index
    first_valid = feature_series.first_valid_index()
    feature = feature_series[first_valid:]

    # window construction
    df_feature = pd.DataFrame(columns=[i for i in range(win)])
    for i in range(0, len(feature) - win, step):
        index = feature.index[i + win - 1]
        df_feature.loc[index] = feature.iloc[i: i + win].values

    # if the dataframe does not include the last date of the series, add it to make sure we always include newest data
    if df_feature.index[-1] != feature.index[-1]:
        index = feature.index[-1]
        df_feature.loc[index] = feature.iloc[-win:].values

    # normalize (min_max)
    df_feature = (df_feature - df_feature.min(1).values.reshape(-1, 1)) / (
            df_feature.max(1).values.reshape(-1, 1) - df_feature.min(1).values.reshape(-1, 1))
    return df_feature


def temporal_cluster(df_feature, start_k=2, end_k=2, n_train=1):
    """
    time series k-means
    1. run the model multiple time for 1 k choose the best model with silhoute score for that k
    2. run different k to pick the best k
    during coding I fix the random state and only run each k once, also limit other parameter to make
    :param df_feature:
    :param start_k:
    :param end_k:
    :param n_train:
    :return:
    """

    best_score = -1
    best_model = None
    for k in range(start_k, end_k + 1):
        for count_train in range(n_train):
            # grid_params = {'eps': eps, 'min_samples': min_samples}
            # model = GridSearchCV(DBSCAN(metric=lambda a, b: DTW.distance(a, b)),
            #                      grid_params, scoring='accuracy', cv=10, n_jobs=-1, verbose=0)

            model = TimeSeriesKMeans(n_clusters=k, metric="dtw")
            y_pred = model.fit_predict(df_feature)
            # model_dbscan = DBSCAN(eps=model.best_params_['eps'],
            #                       min_samples=model.best_params_['min_samples'],
            #                       metric=lambda a, b: DTW.distance(a, b))

            # silhouette score from a sample of 1000 (too expensive to run all)
            score = silhouette_score(df_feature, y_pred, metric="dtw")
            if score > best_score:
                best_score = score
                best_model = model

    return best_model, best_score


def df_temporal_cluster(df, win_size, start_k=2, end_k=2, n_train=1):
    """
    temporal clustering for the whole data frame, using for loop
    :param df:
    :param win_size:
    :param start_k:
    :param end_k:
    :param n_train:
    :return:
    """
    model_info = pd.DataFrame(columns=['Optimal w', 'Optimal k-clusters', 'Average silhouette score'])
    for col in df:
        feature_series = sliding_window(df[col], win_size, step=1)
        model, score = temporal_cluster(feature_series, start_k, end_k, n_train)
        # number of cluster
        k = model.n_clusters
        # model name
        filename = str(col) + '_k' + str(k) + '_w' + str(win_size) + '_model'
        # save model
        model.to_pickle(filename)
        # create dataframe
        model_info.loc[col] = [win_size, k, score]
    # save csv file
    model_info.to_csv(r'./data/outputs/temporal_kmeans_info.csv')


def graph_cluster(df_feature, model, y_pred):
    """
    Graphing function
    :param df_feature:
    :param model:
    :param y_pred:
    :return:
    """
    col = min(3, model.n_clusters)
    row = math.ceil(model.n_clusters/col)
    fig, axs = plt.subplots(row, col, figsize=(15, 10))
    if row == 1:
        axs = np.reshape(axs, (-1, 2))
    for yi in range(model.n_clusters):
        # row that subplot belongs
        rw = math.floor(yi/col)
        # col that subplot belongs
        cl = (yi % col)
        axs[rw, cl].plot(df_feature[y_pred == yi].sample(5).T, "k-", alpha=.2)
        axs[rw, cl].plot(model.cluster_centers_[yi], "r-")
        axs[rw, cl].title.set_text("DBA $k$-means Cluster %d" % (yi + 1))
    fig.tight_layout()


def feature_transformer(df, win_size):
    """

    :param df:
    :param win_size:
    :return:
    """
    # find the latest first valid
    latest_valid = max([df[col].first_valid_index() for col in df])
    # find start point of df
    df_start_index = df.reset_index()[df.index == latest_valid].index[0] + win_size - 1
    df_start_date = df[df.reset_index().index == df_start_index].index[0]

    df_train_all = pd.DataFrame()
    df_test_all = pd.DataFrame()
    for col in df.columns:
        model = TimeSeriesKMeans.from_pickle(col)
        # find the start date of col
        col_win = model[col][2]
        col_start_index = df_start_index-col_win+1
        # create sliding window
        X = sliding_window(df[df.reset_index().index >= col_start_index][col], col_win)
        X_fitted = model[col][0].transform(X)
        df_transform = pd.DataFrame(X_fitted, index=X.index)
        # split into test and train set
        df_train_transform = df_transform[df_transform.index < split_date].add_prefix(col+'_feature')
        df_test_transform = df_transform[df_transform.index >= split_date].add_prefix(col+'_feature')
        df_train_all = pd.concat([df_train_all, df_train_transform], axis=1)
        df_test_all = pd.concat([df_test_all, df_test_transform], axis=1)

    return df_train_all, df_test_all


if __name__ == "__main__":
    # read train data file
    File = '/ffd_train_split2018-01-01'
    df_train = pd.read_csv(File)

    # set date as index
    df_train = df_train.set_index('Date')

    # read test data file
    File = '/ffd_test_split2018-01-01_end2019-01-01'
    df_test = pd.read_csv(File)

    # set date as index
    df_test = df_test.set_index('Date')

    # split date
    split_date = df_test.index[0]

    # concat df_train and df_test since we perform transformation on both set using the same clusters
    df = pd.concat([df_train, df_test], axis=0)

    df_test = pd.read_csv(r".\data\temp_datasets\ffd_test_split2018-01-01_end2019-01-01.csv").set_index('Date')
    df_train = pd.read_csv(r".\data\temp_datasets\ffd_train_split2018-01-01.csv").set_index('Date')
