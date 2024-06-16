import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def filter_data(df, **filters):
    for column, value in filters.items():
        df = df[df[column] == value]
    return df
