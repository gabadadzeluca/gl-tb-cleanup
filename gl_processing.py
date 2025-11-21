import pandas as pd
from columns_to_keep import COLUMNS_GL


def load_excel(filename: str) -> pd.DataFrame:
    try:
        return pd.read_excel(filename)
    except FileNotFoundError:
        raise FileNotFoundError(f"{filename} not found.")


def filter_columns(df: pd.DataFrame) -> pd.DataFrame:
    #Keep only columns defined in COLUMNS_GL
    existing_cols = {
        eng: geo for eng, geo in COLUMNS_GL.items()
        if geo in df.columns
    }
    return df[list(existing_cols.values())]


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    #Convert date column to datetime original format DD/MM/YYYY
    date_geo = COLUMNS_GL.get("date")

    if date_geo in df.columns:
        df[date_geo] = pd.to_datetime(
        df[date_geo].astype(str).str.strip(),
        format="%d/%m/%Y",
        errors="coerce"
    ).dt.date

    return df

def insert_after(df: pd.DataFrame, after_col: str, new_col: str, values):
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
    #Add DR_left and CR_left based on first 4 characters.
    debit_geo  = COLUMNS_GL["acc_debit"]
    credit_geo = COLUMNS_GL["acc_credit"]

    df.loc[:, "DR_left"] = df[debit_geo].astype(str).str[:4]
    df.loc[:, "CR_left"] = df[credit_geo].astype(str).str[:4]

    df = insert_after(df, debit_geo, "DR_left", df["DR_left"])
    df = insert_after(df, credit_geo, "CR_left", df["CR_left"])

    return df


def remove_noncash_transactions(df: pd.DataFrame) -> pd.DataFrame:
    #Remove rows where both debit and credit accounts do not start with '1'
    debit_geo  = COLUMNS_GL["acc_debit"]
    credit_geo = COLUMNS_GL["acc_credit"]

    mask_prev= (
      df[debit_geo].astype(str).str.startswith(('11','12')) |
      df[credit_geo].astype(str).str.startswith(('11','12'))
    )
    mask_both_cash = (
      df[debit_geo].astype(str).str.startswith(('11', '12')) &
      df[credit_geo].astype(str).str.startswith(('11', '12'))  
    )
    mask_final = mask_prev & ~mask_both_cash
    return df[mask_final]

def add_grouping_column(df: pd.DataFrame) -> pd.DataFrame:
     # Insert an empty column at position 0 (first column)
    df.insert(0, "Grouping", "") #empty string for now
    return df

def add_month_column(df: pd.DataFrame) -> pd.DataFrame:
    date_geo = COLUMNS_GL.get("date")
    if date_geo in df.columns:
        df["Month"] = pd.to_datetime(df[date_geo]).dt.month
    return df

# TODO CHECKS FOR NEGATIVE VALUES 


def process_gl(df: pd.DataFrame) -> pd.DataFrame:
    df = filter_columns(df)
    df = parse_dates(df)
    df = add_left_account_codes(df)
    df = remove_noncash_transactions(df)
    df = add_grouping_column(df)
    df = add_month_column(df)
    return df
