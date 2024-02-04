import io
import os
import requests
import pandas as pd
from io import BytesIO
import warnings 
from google.cloud import storage


"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

# services = ['fhv','green','yellow']
init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
# switch out the bucketname
#BUCKET = os.environ.get("GCP_GCS_BUCKET", "dtc-data-lake-bucketname")
BUCKET = os.environ.get("GCP_GCS_BUCKET", "mage-zoomcamp-lulu-eu")


def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)
    
def web_to_gcs(year, service):
    if service == 'yellow':
        data_types = {
            'VendorID': 'float64',
            'passenger_count': 'float64',
            'trip_distance': 'float64',
            'RatecodeID': 'float64',
            'store_and_fwd_flag': 'object',
            'PULocationID': 'int64',
            'DOLocationID': 'int64',
            'payment_type': 'float64',
            'fare_amount': 'float64',
            'extra': 'float64',
            'mta_tax': 'float64',
            'tip_amount': 'float64',
            'tolls_amount': 'float64',
            'improvement_surcharge': 'float64',
            'total_amount': 'float64',
            'congestion_surcharge': 'float64'
        }
        date_cols = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']

    elif service == 'green':
        data_types = {
            'VendorID': 'float64',
            'passenger_count': 'float64',
            'trip_distance': 'float64',
            'RatecodeID': 'float64',
            'store_and_fwd_flag': 'object',
            'PULocationID': 'int64',
            'DOLocationID': 'int64',
            'payment_type': 'float64',
            'fare_amount': 'float64',
            'extra': 'float64',
            'mta_tax': 'float64',
            'tip_amount': 'float64',
            'tolls_amount': 'float64',
            'improvement_surcharge': 'float64',
            'total_amount': 'float64',
            'payment_type': 'float64',
            'trip_type': 'float64',
            'congestion_surcharge': 'float64'
        }
        date_cols = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']
    
    elif service == 'fhv':
        data_types = {
            'dispatching_base_num': 'object',
            'PUlocationID': 'float64',
            'DOlocationID': 'float64',
            'SR_Flag': 'float64',
            'Affiliated_base_number': 'object',
        }
        date_cols = ['pickup_datetime', 'dropOff_datetime']
    
    else:
        warnings.warn(f"Unknown service: {service}. Please use 'yellow', 'green', or 'fhv'.")
        return
        
    for i in range(12):
        
        # sets the month part of the file_name string
        months = [f'{mon:02}' for mon in range(1, 13)]
        month = months[i]

        # csv file_name
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"
        
        # read into a df
        url = f"{init_url}{service}/{file_name}"
        print(url)
        r = requests.get(url)
        df_csv = pd.read_csv(BytesIO(r.content), compression='gzip', dtype=data_types, parse_dates=date_cols)
        
        # define column dtypes and convert to lower
        df_csv.columns = map(str.lower, df_csv.columns)
        
        # Convert DataFrame to Parquet format in memory
        file_name = file_name.replace('.csv.gz', '.parquet')
        df_csv.to_parquet(file_name, engine='pyarrow')
        print(f"Parquet: {file_name}")
        
        # Upload Parquet data to GCS
        gcs_object_name = f"{service}/{file_name}"
        print(f'Bucket: {BUCKET}   Object: {gcs_object_name}')
        upload_to_gcs(BUCKET, gcs_object_name, file_name)
        print(f"GCS: {gcs_object_name}")
        
        # Check if the file exists locally before attempting to delete it
        if os.path.exists(file_name): 
            os.remove(file_name)
            print(f"Local file {file_name} deleted.")
        else:
            print(f"Local file {file_name} does not exist.")


web_to_gcs('2019', 'green')
#web_to_gcs('2020', 'green')
#web_to_gcs('2019', 'yellow')
#web_to_gcs('2020', 'yellow')
#web_to_gcs('2019', 'fhv')