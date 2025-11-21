import pandas as pd
from mappings import LOOKUP_MAP


def find_mapping_for_row(dr_left: str, cr_left: str) -> str:
  for(dr_prefix, cr_prefix), mapping in LOOKUP_MAP.items():
    if dr_left.startswith(dr_prefix) and cr_left.startswith(cr_prefix):
        return mapping
  return "Unmapped"

def add_groupings(df: pd.DataFrame) -> pd.DataFrame:
    # df = lookup(df)
    return df
