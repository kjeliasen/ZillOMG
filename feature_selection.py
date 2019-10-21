###############################################################################
### python imports                                                          ###
###############################################################################

print('Getting Feature Selection', __name__)

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


###############################################################################
### local imports                                                           ###
###############################################################################

from split_scale import wrangle_zillow, get_sql, get_db_url
from split_scale import get_base_df, get_gross_df, rename_fields
from split_scale import xy_df, set_context, df_join_xy, pairplot_train, heatmap_train
from split_scale import split_my_data_xy, split_my_data
from split_scale import scalem, scale_inverse
from split_scale import standard_scaler, uniform_scaler, gaussian_scaler, min_max_scaler, iqr_robust_scaler




#OLS object to analyze features

# ols_model = sm.OLS(y_train,X_train)
# fit = ols_model.fit()
# fit.summary()

#ols_model = ols('y_train ~ X_train',data=train).fit()
#train['yhat'] = ols_model.predict(y_train)


print('Got Feature Selection')