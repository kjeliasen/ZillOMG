###############################################################################
### imports                                                                 ###
###############################################################################

import warnings
warnings.filterwarnings("ignore")

import numpy as np
# import viz
# import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns
from acquire import wrangle_zillow, get_sql, get_db_url


###############################################################################
### get data from acquire                                                   ###
###############################################################################


def get_gross_df(db='zillow', sql='zillow_sql', sql_string=False):
    '''
    get_gross_df(db='zillow', sql='zillow_sql', sql_string=False)
    RETURNS gross_df

    Pulls gross dataset from source database.
    '''
    
    gross_df = wrangle_zillow(db=db, sql=sql, sql_string=sql_string)
    return gross_df


def rename_fields():
    name_flip = {
        'parcelid':'pid',
        'bathroomcnt':'nbr_bedrms',
        'bedroomcnt':'nbr_bthrms',
        'calculatedfinishedsquarefeet':'finished_sqft',
        'taxvaluedollarcnt':'taxable_value',
        '':'',
        '':'',
        '':'',
        '':'',
        '':'',
        '':'',
        '':'',
        '':'',
        '':'',
        '':'',
        '':''
    }

def get_base_df():
    '''
    set_base_df()
    RETURN base_df

    Gets basic dataframe for MVP objective. Features include bathrooms, 
    bedrooms, and square footage. Target variable is 'taxvaluedollarcnt'
    
    
    '''

    keep_fields = ['bathroomcnt','bedroomcnt','calculatedfinishedsquarefeet','taxvaluedollarcnt','parcelid']
    gross_df = get_gross_df()[keep_fields]
    base_df = gross_df.set_index('parcelid')

    return base_df
