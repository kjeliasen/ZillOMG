###############################################################################
### imports                                                                 ###
###############################################################################

print('Getting Prep', __name__)

import warnings
warnings.filterwarnings("ignore")

import numpy as np
# import viz
# import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns
from acquire import wrangle_zillow, get_sql, get_db_url


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


print('get gross df')
def get_gross_df(db='zillow', sql='zillow_sql', sql_string=False):
    '''
    get_gross_df(db='zillow', sql='zillow_sql', sql_string=False)
    RETURNS dataframe

    Pulls gross dataset from source database. Fields will be renamed according to rules set in rename_fields()
    '''
    orig_df = wrangle_zillow(db=db, sql=sql, sql_string=sql_string)
    print(orig_df.info())
    new_df = rename_fields(orig_df)
    print(new_df.info())
    return new_df


print('rename fields')
def rename_fields(dataframe):
    '''
    rename_fields(dataframe)
    
    '''
    columns = dataframe.columns.tolist()
    print(columns)
    renames = {k: v for k, v in _global_renames if k in columns}
    print(renames)
    new_df = dataframe.rename(columns=renames)
    return new_df


print('get base df')
def get_base_df():
    '''
    set_base_df()
    RETURN base_df

    Gets basic dataframe for MVP objective. Features include bathrooms, 
    bedrooms, and square footage. Target variable is 'taxvaluedollarcnt'
    
    
    '''
    keep_fields = ['nbr_bthrms','nbr_bedrms','finished_sqft','taxable_value']
    gross_df = get_gross_df()
    print(gross_df.head())
    base_df = gross_df[keep_fields] #.set_index('id')

    return base_df


print('Got Prep')