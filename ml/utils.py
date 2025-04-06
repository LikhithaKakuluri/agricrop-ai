def normalize_columns(df):
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("-", "_")
    return df
