import pandas as pd

def nan_null_zero_datatypes(df):
    have_values = [(df[col].notna() & (df[col] != 0)).sum() for col in df.columns]
    nans = [df[col].isna().sum() for col in df.columns]
    blanks = [(df[col] == ' ').sum() for col in df.columns]
    zeros = [(df[col] == 0).sum() for col in df.columns]
    data_types = [df[col].apply(lambda x: type(x)).unique() for col in df.columns]
    len_data_types = [len(df[col].apply(lambda x: type(x)).unique()) for col in df.columns] 
    

    df_clean_check = pd.DataFrame({
        'Column Name': df.columns,
        'have_values': have_values,
        '# NAs': nans,
        '# Blanks': blanks,
        '# Zeros': zeros,
        '# Data Types': len_data_types,
        'Data Types': data_types
    })

    return df_clean_check