# HAVE TO RUN THIS FIRST IN THE TERMINAL 
# sudo chmod -R 777 ny_taxi_postgres_data

FROM python:3.9.1

RUN apt-get update && apt-get install wget
RUN pip install --upgrade pip
RUN pip install pandas sqlalchemy psycopg2 pyarrow

WORKDIR /app
COPY data-ingest.py data-ingest.py

ENTRYPOINT [ "python", "data-ingest.py" ]