###############################################################################
### imports                                                                 ###
###############################################################################

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from debug import local_settings, timeifdebug, timeargsifdebug


_global_renames = (
    ('parcelid', 'pid'),
    ('bathroomcnt', 'nbr_bedrms'),
    ('bedroomcnt', 'nbr_bthrms'),
    ('calculatedfinishedsquarefeet', 'finished_sqft'),
    ('taxvaluedollarcnt', 'taxable_value'),
)


###############################################################################
### get data from acquire                                                   ###
###############################################################################


@timeifdebug
def edit_gross_df(dataframe):
    '''
    get_acquire_df(dataframe)
    RETURNS dataframe with columns renamed

    Fields will be renamed according to rules set in rename_fields()
    '''
    return rename_fields(dataframe)


@timeifdebug
def rename_fields(dataframe):
    '''
    rename_fields(dataframe)
    
    '''
    columns = dataframe.columns.tolist()
    renames = {k: v for k, v in _global_renames if k in columns}
    new_df = dataframe.rename(columns=renames)
    return new_df


@timeifdebug
def edit_prep_df(dataframe):
    '''
    set_base_df(dataframe)
    RETURN prepped_df

    Gets basic dataframe for MVP objective. Features include bathrooms, 
    bedrooms, and square footage. Target variable is 'taxable_value'
    '''

    keep_fields = ['nbr_bthrms','nbr_bedrms','finished_sqft','taxable_value']
    prepped_df = dataframe[keep_fields]

    return prepped_df


# print('Got Prep')