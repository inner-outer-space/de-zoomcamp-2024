import io
import os
import requests
import pandas as pd
from io import BytesIO
import warnings 
from google.cloud import storage
import time 

# ADDED A 60 SECOND PAUSE TO AVOID OVERLOADING THE SERVER

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
BUCKET = os.environ.get("GCP_GCS_BUCKET", "mage-zoomcamp-lulu")


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
    full_df_csv = pd.DataFrame()
    for i in range(12):
        
        # sets the month part of the file_name string
        months = [f'{mon:02}' for mon in range(1, 13)]
        month = months[i]

        # csv file_name
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"
        
        # read into a large df
        url = f"{init_url}{service}/{file_name}"
        print(url)
        r = requests.get(url)
        df_csv = pd.read_csv(BytesIO(r.content), compression='gzip')
        
        full_df_csv = pd.concat([full_df_csv, df_csv], ignore_index=True)
        
        time.sleep(60)

    # modify date columns and fix column names 
            
    # create a parquet file
    file_name = f"{service}_trip_data_{year}.parquet"
    full_df_csv.to_parquet(file_name, engine='pyarrow')
    print(f"Parquet: {file_name}")

    # upload it to gcs 
    print(f'Bucket: {BUCKET}   Object: {service}/{file_name}')
    upload_to_gcs(BUCKET, f"{service}/{file_name}", file_name)
    print(f"GCS: {service}/{file_name}")


web_to_gcs('2019', 'green')
#web_to_gcs('2020', 'green')
#web_to_gcs('2019', 'yellow')
#web_to_gcs('2020', 'yellow')
#web_to_gcs('2019', 'fhv')