import pandas as pd
from utils.columns_to_keep import COLUMNS_TB

# For accessing the left(4) account code
from core.tb_processing import ACC_LEFT

# Test for now
PPE_PREFIXES = ['163','21']
""" might need to change 163 -> 1635"""

def process_ppe(df: pd.DataFrame) -> pd.DataFrame:
   acc  = COLUMNS_TB["acc"]

   acc_str = df[ACC_LEFT].astype(str)
   acc_num = pd.to_numeric(acc_str, errors="coerce")

   mask_ppe = (
      acc_str.str.startswith(tuple(PPE_PREFIXES)) &
      # Exclude accounts ending with 000, 00
      (acc_num % 1000 != 0) &
      (acc_num % 100 != 0)
   )
   df = df[mask_ppe]

   return df
