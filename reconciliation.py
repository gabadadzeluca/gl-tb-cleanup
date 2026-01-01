import pandas as pd
from openpyxl.utils import get_column_letter
from columns_to_keep import COLUMNS_GL
from columns_to_keep import COLUMNS_TB


START_ROW = 4  # leaves rows 1–3 free for headers
SHEET_NAME = "TB&GL Reconciliation"

def build_recon_skeleton(tb_df):
    return pd.DataFrame({
        "Account": extract_needed_accounts(tb_df),
        "Description": None,
        "Movement DR (TB)": None,
        "Movement CR (TB)": None,
        "Movement DR (GL)": None,
        "Movement CR (GL)": None,
        "Check DR": None,
        "Check CR": None,
    })

def extract_needed_accounts(tb_df):
  acc_str = tb_df[COLUMNS_TB["acc"]].str.strip()


  numeric_acc = pd.to_numeric(acc_str, errors='coerce')

  # accounts that are exactly 4 digits and not ending with 00
  mask1 = (acc_str.str.len() == 4) & \
          (acc_str.str.isdigit()) & \
          (numeric_acc % 100 != 0)

  # accounts that start with letters: eg: B600
  mask2 = (acc_str.str.len() == 4) & (acc_str.str[:1].str.isalpha())
  mask = mask1 | mask2

  return acc_str[mask]

def fill_excel(ws, recon_df: pd.DataFrame, company_name) -> None:
    # Add header
    ws["A1"] = f"TB & GL Reconciliation of {company_name}" if company_name else "TB & GL Reconciliation"
    ws["A2"] = "Reporting Date:"

    #Set column widths
    for col_idx, column_cells in enumerate(ws.columns, start=1):
        max_length = 0
        column = get_column_letter(col_idx)
        for cell in column_cells:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

def reconcile_data(tb_df: pd.DataFrame, gl_df: pd.DataFrame, writer: pd.ExcelWriter, company_name) -> None:

    # 1. Build the reconciliation base table (structure only)
    recon_df = build_recon_skeleton(tb_df)

    # 2. Write raw data
    recon_df.to_excel(
      writer,
      sheet_name=SHEET_NAME,
      index=False,
      startrow=START_ROW - 1  # pandas is 0-based
    )

    ws = writer.sheets[SHEET_NAME]
    fill_excel(ws, recon_df, company_name)


    # 3. Inject Excel formulas
    # add_reconciliation_formulas(ws, recon_df)
    return recon_df # test
