import pandas as pd
from columns_to_keep import COLUMNS_TB

# Test for now
PPE_PREFIXES = ['16','21']

def process_ppe(df: pd.DataFrame) -> pd.DataFrame:
   acc  = COLUMNS_TB["acc"]

   mask_ppe = df[acc].astype(str).str.startswith(tuple(PPE_PREFIXES))
   df = df[mask_ppe]

   return df
