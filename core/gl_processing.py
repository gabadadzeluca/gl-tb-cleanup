import pandas as pd
from utils.columns_to_keep import COLUMNS_GL_1C, COLUMNS_GL_2C
from common.cleanup import clean_df

DR_LEFT = "DR_left"
CR_LEFT = "CR_left"

def add_grouping_column(df: pd.DataFrame) -> pd.DataFrame:
    # Insert an empty column at position 0 (first column)
    df.insert(0, "Grouping", "") #empty string for now
    return df

# TODO CHECKS FOR NEGATIVE VALUES 

def insert_after(df: pd.DataFrame, after_col: str, new_col: str, values):
    df = df.copy()  # avoid SettingWithCopyWarning
    # create or update the column
    df[new_col] = values

    # reorder: remove column and re-insert at correct position
    cols = list(df.columns)
    cols.remove(new_col)
    idx = cols.index(after_col) + 1
    cols.insert(idx, new_col)

    df = df[cols]
    return df

def add_left_account_codes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy() # copy to prevent an error
    
    # add DR_left and CR_left based on first 4 characters.
    debit_geo  = COLUMNS_GL["acc_debit"]
    credit_geo = COLUMNS_GL["acc_credit"]

    df.loc[:, DR_LEFT] = df[debit_geo].astype(str).str[:4]
    df.loc[:, CR_LEFT] = df[credit_geo].astype(str).str[:4]

    df = insert_after(df, debit_geo, DR_LEFT, df[DR_LEFT])
    df = insert_after(df, credit_geo, CR_LEFT, df[CR_LEFT])

    return df

def process_gl(df: pd.DataFrame, is_1C_format: bool) -> pd.DataFrame:
    if(is_1C_format):
        COLUMNS_GL = COLUMNS_GL_1C
    else:
        COLUMNS_GL = COLUMNS_GL_2C
    
    df = clean_df(df, col_map=COLUMNS_GL)
    df = add_left_account_codes(df)
    df = add_grouping_column(df)
    return df
