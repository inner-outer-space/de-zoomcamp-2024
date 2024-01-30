## Week 2 Homework

For the homework, we'll be working with the _green_ taxi dataset located here:

`https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green`

### Assignment

The goal will be to construct an ETL pipeline that loads the data, performs some transformations, and writes the data to a database (and Google Cloud!).

- Create a new pipeline, call it `green_taxi_etl`
- Add a data loader block and use Pandas to read data for the final quarter of 2020 (months `10`, `11`, `12`).
  - You can use the same datatypes and date parsing methods shown in the course.
  - `BONUS`: load the final three months using a for loop and `pd.concat`
- Add a transformer block and perform the following:
  - Remove rows where the passenger count is equal to 0 _or_ the trip distance is equal to zero.
  - Create a new column `lpep_pickup_date` by converting `lpep_pickup_datetime` to a date.
  - Rename columns in Camel Case to Snake Case, e.g. `VendorID` to `vendor_id`.
  - Add three assertions:
    - `vendor_id` is one of the existing values in the column (currently)
    - `passenger_count` is greater than 0
    - `trip_distance` is greater than 0
- Using a Postgres data exporter (SQL or Python), write the dataset to a table called `green_taxi` in a schema `mage`. Replace the table if it already exists.
- Write your data as Parquet files to a bucket in GCP, partioned by `lpep_pickup_date`. Use the `pyarrow` library!
- Schedule your pipeline to run daily at 5AM UTC.

#### DATA LOADER 
``` python
@data_loader
def load_data_from_api(*args, **kwargs):
    year = '2020'
    months = ['10', '11', '12']
    full_df = pd.DataFrame()

    for mon in months: 
        url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-{mon}.csv.gz'
        df = pd.read_csv(url, compression='gzip')
        
        full_df = pd.concat([full_df, df], ignore_index=True)
        print(mon, df.shape, "full:", full_df.shape)

    return full_df
```
#### TRANSFORMER 
```python

@transformer
def transform(data, *args, **kwargs):
    # change columns to snake_case
    data.columns = data.columns.str.lower()

    # filter out rows with passenger_count = 0 or trip_distance = 0
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]

    # add a date column based on the date time column
    data.lpep_pickup_datetime= pd.to_datetime(data.lpep_pickup_datetime)
    data.lpep_dropoff_datetime= pd.to_datetime(data.lpep_dropoff_datetime)
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date 
    print(data.shape)
    return data


@test
def test_output(output, *args) -> None:
    assert 'vendorid' in output.columns, 'vendorid does not exist'
    
@test
def test_output(output, *args) -> None:
    assert output['passenger_count'].isin([0]).sum() ==0, 'There are rides with zero passengers'

@test
def test_output(output, *args) -> None:
    assert output['trip_distance'].isin([0]).sum() ==0,'There are rides distance = 0'
```






### Questions

## Question 1. Data Loading

Once the dataset is loaded, what's the shape of the data?

* 266,855 rows x 20 columns ***THIS ONE***
* 544,898 rows x 18 columns
* 544,898 rows x 20 columns
* 133,744 rows x 20 columns

## Question 2. Data Transformation

Upon filtering the dataset where the passenger count is equal to 0 _or_ the trip distance is equal to zero, how many rows are left?

* 544,897 rows
* 266,855 rows
* 139,370 rows ***THIS ONE***
* 266,856 rows


## Question 3. Data Transformation

Which of the following creates a new column `lpep_pickup_date` by converting `lpep_pickup_datetime` to a date?

* data = data['lpep_pickup_datetime'].date
* data('lpep_pickup_date') = data['lpep_pickup_datetime'].date
* data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date  ***THIS ONE***
* data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt().date()

## Question 4. Data Transformation

What are the existing values of `VendorID` in the dataset?

* 1, 2, or 3
* 1 or 2   ***THIS ONE***
* 1, 2, 3, 4
* 1

```python 
value_counts= data['vendorid'].value_counts()
value_counts
```

## Question 5. Data Transformation

How many columns need to be renamed to snake case?

* 3
* 6
* 2
* 4  ***THIS ONE***

## Question 6. Data Exporting

Once exported, how many partitions (folders) are present in Google Cloud?  ***I GET 95 for the days and then 1 for green taxi***

* 96 ***THIS ONE***
* 56
* 67
* 108

## Submitting the solutions

* Form for submitting: TBA 

Deadline: TBA

## Solution

Will be added after the due date
