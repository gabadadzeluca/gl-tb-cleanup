import pandas as pd


def load_excel(filename: str) -> pd.DataFrame:
    try:
        return pd.read_excel(filename)
    except FileNotFoundError:
        raise FileNotFoundError(f"{filename} not found.")

def filter_columns(df: pd.DataFrame, col_map: dict[str, str]) -> pd.DataFrame:
    #Keep only columns defined in COLUMNS_TO_KEEP
    existing_cols = {
        eng: geo for eng, geo in col_map.items()
        if geo in df.columns
    }
    return df[list(existing_cols.values())]


def parse_dates(df: pd.DataFrame, col_map: dict[str, str]) -> pd.DataFrame:
    #Convert date column to datetime original format DD/MM/YYYY
    date_geo = col_map.get("date")

    if date_geo in df.columns:
        df[date_geo] = pd.to_datetime(
        df[date_geo].astype(str).str.strip(),
        format="%d/%m/%Y",
        errors="coerce"
    ).dt.date

    return df

def add_grouping_column(df: pd.DataFrame) -> pd.DataFrame:
     # Insert an empty column at position 0 (first column)
    df.insert(0, "Grouping", "") #empty string for now
    return df

def add_month_column(df: pd.DataFrame, col_map: dict[str, str]) -> pd.DataFrame:
    date_geo = col_map.get("date")
    if date_geo in df.columns:
        df["Month"] = pd.to_datetime(df[date_geo]).dt.month
    return df

def clean_df(df: pd.DataFrame, col_map: dict[str, str]) -> pd.DataFrame:
    df = filter_columns(df, col_map)
    df = parse_dates(df, col_map)
    df = add_month_column(df, col_map)
    return df
