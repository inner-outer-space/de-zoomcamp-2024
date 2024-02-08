import pandas as pd
from io import BytesIO
import requests
import warnings


def nan_null_zero_datatypes(df):
    """
    This function returns a summary information for each column in a dataframe:
    - NaN counts
    - blank counts
    - zero counts
    - dtypes
    - unique dtype counts

    Args:
        df (DataFrame): The DataFrame that you want to check.

    Returns:
        DataFrame: A DataFrame containing the following information for each column:
        - 'Column Name': The column names.
        - 'have_values': Count of non-null and non-zero values.
        - '# NAs': Count of NaN values.
        - '# Blanks': Count of blank (empty string) values.
        - '# Zeros': Count of zero values.
        - '# Data Types': Count of unique data types.
        - 'Data Types': Unique data types.

    Example:
        result = nan_null_zero_datatypes(df)
    """
    
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

def get_service_year_dtypes(service, year, verbose=False):
    """
    There have been data load issues around inconsistent data types in the monthly CSV files for the NYC taxi services.
    
    This function downloads CSV files for each month of the specified year and service, extracts column data types,
    and compiles them into a summary DataFrame.
    
    

    Args:
        service (str):  NYC taxi service ('yellow', 'green', or 'fhv').
        year (int)
        verbose (bool): If True, prints the URL for each CSV file.

    Returns:
        pandas.DataFrame: A DataFrame with columns: months, rows: CSV column name, values: dtypes 

    Example:
        To collect data types for the 'yellow' taxi service in the year 2022:
        
        >>> df = get_year_dtypes('yellow', 2022)
        >>> print(df)
        
        This will output a DataFrame with columns like '01_2022', '02_2022', ..., '12_2022' 
        indicating data types for each month of the specified year.

    Note:
        - The function assumes that monthly CSV files are available and accessible at specified URLs.
        - It may require an internet connection to download data files from URLs.
    """
    warnings.filterwarnings("ignore")
    
    full_dtype_df = pd.DataFrame()
    init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
    
    for i in range(12):
    
        # sets the month part of the file_name string
        months = [f'{mon:02}' for mon in range(1, 13)]
        month = months[i]
        
        # csv file_name
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"

        # read into a df
        url = f"{init_url}{service}/{file_name}"
        if verbose:
            print(url)
        r = requests.get(url)
        df_csv = pd.read_csv(BytesIO(r.content), compression='gzip')
        
        col_name = f'{month}_{year}'
        #data_types = [df_csv[col].apply(lambda x: type(x)).unique() for col in df_csv.columns]
        data_types = [set(type(x).__name__ for x in df_csv[col]) for col in df_csv.columns]
        unique_count = [df_csv[col].nunique() for col in df_csv.columns]

        dtype_df = pd.DataFrame({
            'Column Name': df_csv.columns,
            col_name: data_types,
            f'n_{col_name}': unique_count
        })
        
        dtype_df = dtype_df.set_index('Column Name')
        full_dtype_df = pd.concat([full_dtype_df, dtype_df], axis=1)
        
        # if full_dtype_df.empty:
        #     full_dtype_df = dtype_df  # Initialize full_dtype_df with dtype_df for the first iteration
        # else:
        #     full_dtype_df = pd.merge(full_dtype_df, dtype_df, on='Column Name', how='outer')

    return full_dtype_df
