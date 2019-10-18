###############################################################################
### python imports                                                          ###
###############################################################################

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
# from math import sqrt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, QuantileTransformer, PowerTransformer, RobustScaler, MinMaxScaler


###############################################################################
### local imports                                                           ###
###############################################################################

from aquire import wrangle_zillow, get_sql, get_db_url
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

get_