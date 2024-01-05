import argparse
import os 
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    data_table_name = params.data_table_name
    lookup_table_name = params.lookup_table_name
    data_url = params.data_url
    lookup_url = params.lookup_url
    parquet_name = 'data_output.parquet'
    csv_name = 'lookup_output.csv'
    
    # DOWNLOAD THE DATA
    os.system(f'wget -O {parquet_name} {data_url}')
    os.system(f'wget -O {csv_name} {lookup_url}')
    
    # CREATE A CONNECTION TO THE DB
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # READ THE PARQUET and CSV FILES INTO DATAFRAMES
    df = pd.read_parquet(parquet_name)
    df_zones = pd.read_csv(csv_name)

    # UPLOAD THE DATA TO THE DB
    df.to_sql(name=data_table_name, con=engine, if_exists='replace')
    df_zones.to_sql(name=lookup_table_name, con=engine, if_exists='replace')


# The parser is used to parse the command line arguments which are then passed to the main method. 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest Parquet and CSV files into a PostgreSQL DB')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name')
    parser.add_argument('--data_table_name', help='data table name')
    parser.add_argument('--lookup_table_name', help='zones lookup table name')
    parser.add_argument('--data_url', help='url for data Parquet file')
    parser.add_argument('--lookup_url', help='url for zones lookup CSV file')

    args = parser.parse_args()
    main(args)
