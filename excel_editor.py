import pandas as pd

def read_excel_df(filepath, ws_name):
    df = pd.DataFrame(pd.read_excel(filepath, ws_name))
    return df

def save_to_excel(filepath, df, ws_name):
    df.to_excel(filepath, sheet_name=ws_name, index=False)