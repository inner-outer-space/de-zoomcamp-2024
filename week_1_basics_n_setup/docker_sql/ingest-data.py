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
    table_name = params.table_name
    url = params.url
    parquet_name = 'output.parquet'
    
    # DOWNLOAD THE DATA
    os.system(f'wget -O {parquet_name} {url}')
    
    # CREATE A CONNECTION TO THE DB
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # READ THE PARQUET and CSV FILES INTO DATAFRAMES
    df = pd.read_parquet(parquet_name)

    # UPLOAD THE DATA TO THE DB
    df.to_sql(name=table_name, con=engine, if_exists='replace')


# The parser is used to parse the command line arguments which are then passed to the main method. 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest Parquet and CSV files into a PostgreSQL DB')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name')
    parser.add_argument('--table_name', help='table name')
    parser.add_argument('--url', help='url for data file')

    args = parser.parse_args()
    main(args)


