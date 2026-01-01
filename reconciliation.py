import pandas as pd
from openpyxl.utils import get_column_letter
from columns_to_keep import COLUMNS_GL
from columns_to_keep import COLUMNS_TB


TB_MASK = [COLUMNS_TB["acc"], COLUMNS_TB["name"], COLUMNS_TB["movement_dr"], COLUMNS_TB["movement_cr"]]

def build_recon_skeleton(tb_df):
    return pd.DataFrame({
        "Account": extract_main_accounts(tb_df),
        "Description": None,
        "Movement DR (TB)": None,
        "Movement CR (TB)": None,
        "Movement DR (GL)": None,
        "Movement CR (GL)": None,
        "Check DR": None,
        "Check CR": None,
    })

def extract_main_accounts(tb_df):
  acc_str = tb_df[COLUMNS_TB["acc"]].str.strip()
  mask = (
    acc_str.str.len() == 4
  ) & (
    acc_str.astype(int) % 100 == 0
  )

  return acc_str[mask]

def reconcile_data(tb_df: pd.DataFrame, gl_df: pd.DataFrame, writer: pd.ExcelWriter) -> None:
    sheet_name = "TB&GL Reconciliation"

    # 1. Build the reconciliation base table (structure only)

    # 2. Write raw data
    # recon_df.to_excel(writer, sheet_name=sheet_name, index=False)

    ws = writer.sheets[sheet_name]

    # 3. Inject Excel formulas
    # add_reconciliation_formulas(ws, recon_df)
