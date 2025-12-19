import pandas as pd
from columns_to_keep import COLUMNS_TB
from common.cleanup import clean_df

ACC_LEFT = "Acc_left"

def add_left_for_tb_accounts(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()  # copy to prevent an error

    # add ACC_left based on first 4 characters.
    acc_geo = COLUMNS_TB["acc"]

    df.loc[:, ACC_LEFT] = df[acc_geo].astype(str).str[:4]

    # insert after the account column
    cols = list(df.columns)
    cols.remove(ACC_LEFT)
    idx = cols.index(acc_geo) + 1
    cols.insert(idx, ACC_LEFT)

    df = df[cols]

    return df


def process_tb(df: pd.DataFrame) -> pd.DataFrame:
  df = clean_df(df, col_map=COLUMNS_TB)
  df = add_left_for_tb_accounts(df)
  return df