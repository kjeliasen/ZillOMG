###############################################################################
### python imports                                                          ###
###############################################################################

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# from math import sqrt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, QuantileTransformer, PowerTransformer, RobustScaler, MinMaxScaler


###############################################################################
### local imports                                                           ###
###############################################################################

from prep import wrangle_zillow, get_sql, get_db_url
from prep import get_base_df, get_gross_df, rename_fields


###############################################################################
### generic scaling functions                                               ###
###############################################################################

### Test Train Split ##########################################################
# train, test = train_test_split(df, train_size = .80, random_state = 123)
def split_my_data_xy(df, target_column, train_pct=.75, random_state=None):
    X = df.drop([target_column], axis=1)
    y = pd.DataFrame(df[target_column])
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_pct, random_state=random_state)
    return X_train, X_test, y_train, y_test


def split_my_data(df, train_pct=.75, random_state=None):
    train, test = train_test_split(df, train_size=train_pct, random_state=random_state)
    return train, test


### Transform Data ############################################################
def scalem(scaler, test, train):
    # transform train
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    # transform test
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return train_scaled, test_scaled


def scale_inverse(train_scaled, test_scaled, scaler):
    # If we wanted to return to original values:
    # apply to train
    train_unscaled = pd.DataFrame(scaler.inverse_transform(train_scaled), columns=train_scaled.columns.values).set_index([train_scaled.index.values])
    # apply to test
    test_unscaled = pd.DataFrame(scaler.inverse_transform(test_scaled), columns=test_scaled.columns.values).set_index([test_scaled.index.values])
    return train_unscaled, test_unscaled


### Standard Scaler ###########################################################
def standard_scaler(train, test):
    # create object & fit
    scaler = StandardScaler(copy=True, with_mean=True, with_std=True).fit(train)
    # scale'm
    train_scaled, test_scaled = scalem(scaler=scaler, test=test, train=train)
    return scaler, train_scaled, test_scaled


### Uniform Scaler ############################################################
def uniform_scaler(train, test):
    # create scaler object and fit to train
    scaler = QuantileTransformer(n_quantiles=100, output_distribution='uniform', random_state=123, copy=True).fit(train)
    # scale'm
    train_scaled, test_scaled = scalem(scaler=scaler, test=test, train=train)
    return scaler, train_scaled, test_scaled


### Gaussian (Normal) Scaler ##################################################
def gaussian_scaler(train, test):
    # create scaler object using yeo-johnson method and fit to train
    scaler = PowerTransformer(method='yeo-johnson', standardize=False, copy=True).fit(train)
    # scale'm
    train_scaled, test_scaled = scalem(scaler=scaler, test=test, train=train)
    return scaler, train_scaled, test_scaled



### MinMax Scaler #############################################################
def min_max_scaler(train, test):
    # create scaler object and fit to train
    scaler = MinMaxScaler(copy=True, feature_range=(0,1)).fit(train)
    # scale'm
    train_scaled, test_scaled = scalem(scaler=scaler, test=test, train=train)
    return scaler, train_scaled, test_scaled



### Robust Scaler #############################################################
def iqr_robust_scaler(train, test):
    # create scaler object and fit to train
    scaler = RobustScaler(quantile_range=(25.0,75.0), copy=True, with_centering=True, with_scaling=True).fit(train)
    # scale'm
    train_scaled, test_scaled = scalem(scaler=scaler, test=test, train=train)
    return scaler, train_scaled, test_scaled


###############################################################################
### project-specific scaling functions                                      ###
###############################################################################


def xy_df(dataframe, y_column):
    '''
    FUNCTION
    RETURNS:
    '''

    X_df = dataframe.drop([y_column], axis=1)
    y_df = pd.DataFrame(dataframe[y_column])
    return X_df, y_df


def split_scaled_dfs(target_df=get_base_df(), y_column='taxvaluedollarcnt', train_pct=.75, randomer=None, scaler_fn=standard_scaler):
    '''
    scale_df(target_df=get_base_df(), y_column='taxvaluedollarcnt', train_pct=.75, randomer=None, scaler_fn=standard_scaler)
    RETURNS: X_train, X_train_scaled, X_test, X_test_scaled, y_train, y_train_scaled, y_test, y_test_scaled, scaler

    scaler_fn must be a function
    dummy val added to train and test to allow for later feature selection testing

    '''
    df_dict = {}
    train, test = split_my_data(df=target_df, random_state=randomer)
    df_dict['scaler'], train_scaled, test_scaled = scaler_fn(train=train, test=test)
    train['dummy_val']=1
    train_scaled['dummy_val']=1
    df_dict['X_train'], df_dict['y_train'] = xy_df(dataframe=train, y_column=y_column)
    df_dict['X_test'], df_dict['y_test'] = xy_df(dataframe=test, y_column=y_column)
    df_dict['X_train_scaled'], df_dict['y_train_scaled'] = xy_df(dataframe=train_scaled, y_column=y_column)
    df_dict['X_test_scaled'], df_dict['y_test_scaled'] = xy_df(dataframe=test_scaled, y_column=y_column)
    return df_dict


def pairplot_train(X, y):
    '''
    FUNCTION
    RETURNS:
    '''
    train_plot = X.join(y)
    sns.pairplot(train_plot)
    plt.show()


def heatmap_train(X, y):
    '''
    FUNCTION
    RETURNS:
    '''
    train_plot = X.join(y)
    plt.figure(figsize=(7,5))
    cor = train_plot.corr()
    sns.heatmap(cor, annot=True, cmap=plt.cm.RdBu_r)
    plt.show()


