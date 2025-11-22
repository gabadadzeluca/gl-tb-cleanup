import pandas as pd
from columns_to_keep import COLUMNS_TB
from common.cleanup import clean_df

def process_tb(df: pd.DataFrame) -> pd.DataFrame:
  df = clean_df(df, col_map=COLUMNS_TB)

  return df