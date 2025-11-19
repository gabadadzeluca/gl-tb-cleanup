import pandas as pd
from columns_to_keep import COLUMNS_TO_KEEP


def load_excel(filename: str) -> pd.DataFrame:
    try:
        return pd.read_excel(filename)
    except FileNotFoundError:
        raise FileNotFoundError(f"{filename} not found.")


def filter_columns(df: pd.DataFrame) -> pd.DataFrame:
    #Keep only columns defined in COLUMNS_TO_KEEP
    existing_cols = {
        eng: geo for eng, geo in COLUMNS_TO_KEEP.items()
        if geo in df.columns
    }
    return df[list(existing_cols.values())]


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    #Convert date column to datetime original format DD/MM/YYYY
    date_geo = COLUMNS_TO_KEEP.get("date")

    if date_geo in df.columns:
        df[date_geo] = pd.to_datetime(
        df[date_geo].astype(str).str.strip(),
        format="%d/%m/%Y",
        errors="coerce"
    ).dt.date

    return df


def add_left_account_codes(df: pd.DataFrame) -> pd.DataFrame:
    #Add DR_left and CR_left based on first 4 characters.
    debit_geo  = COLUMNS_TO_KEEP["acc_debit"]
    credit_geo = COLUMNS_TO_KEEP["acc_credit"]

    df["DR_left"] = df[debit_geo].astype(str).str[:4]
    df["CR_left"] = df[credit_geo].astype(str).str[:4]

    return df


def process_gl(df: pd.DataFrame) -> pd.DataFrame:
    df = filter_columns(df)
    df = parse_dates(df)
    df = add_left_account_codes(df)
    return df
