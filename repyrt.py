import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# from math import sqrt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, QuantileTransformer, PowerTransformer, RobustScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score

import statsmodels.api as sm
from statsmodels.formula.api import ols

from debug import local_settings, timeifdebug, timeargsifdebug

from acquire import wrangle_zillow, get_sql, get_db_url, frame_splain
from prep import edit_gross_df, edit_prep_df, rename_fields
from split_scale import xy_df, set_context, df_join_xy, pairplot_train, heatmap_train
from split_scale import split_my_data_xy, split_my_data
from split_scale import scalem, scale_inverse
from split_scale import standard_scaler, uniform_scaler, gaussian_scaler, min_max_scaler, iqr_robust_scaler




@timeifdebug
def acquire_data(db='zillow', sql='zillow_sql', sql_string=False):
    return wrangle_zillow(db=db, sql=sql, sql_string=sql_string)


@timeifdebug
def prep_data(acquire_df):
    gross_df = edit_gross_df(acquire_df)
    return edit_prep_df(gross_df)


