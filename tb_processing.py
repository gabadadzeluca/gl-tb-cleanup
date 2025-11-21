import pandas as pd
from common.cleanup import clean_df

def process_tb(df: pd.DataFrame) -> pd.DataFrame:
   #TODO process TB data
  df = clean_df(df)
  ...
  return df