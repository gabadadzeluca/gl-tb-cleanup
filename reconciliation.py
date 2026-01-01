import pandas as pd
from columns_to_keep import COLUMNS_GL
from columns_to_keep import COLUMNS_TB


# receive cleaned TB and GL dataframes
def reconcile_data(tb_df: pd.DataFrame, gl_df: pd.DataFrame) -> pd.DataFrame:
  # leave only the main accounts from the TB
  ...