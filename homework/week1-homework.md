## Module 1 Homework

## Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 

- `--delete`
- `--rc`
- `--rmc`
- `--rm` **THIS ONE**


## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?

- 0.42.0 **THIS ONE**
- 1.0.0
- 23.0.1
- 58.1.0


# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

***Note: I used the parquet file instead of the CSV. There is a difference in the Vendor ID column between the parquet and csv. The rest of the data looks like it is the same. On the other hang, the CSV and parquet files for Jan 2019 (2023 HW) are very different. ***


## Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 15767
- 15612  **This ONe**
- 15859
- 89009

```sql
SELECT 
	count(*)
FROM 
	green_taxi_trips
WHERE 
	CAST(lpep_pickup_datetime AS date) = '2019-09-18'
	AND CAST(lpep_dropoff_datetime AS date) = '2019-09-18';
```

## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

- 2019-09-18
- 2019-09-16
- 2019-09-26  **This one with trip dist = 341.64**
- 2019-09-21

```sql
SELECT 
	CAST(lpep_pickup_datetime AS date) as pu_date,
	trip_distance
	
FROM 
	green_taxi_trips
ORDER BY trip_distance DESC
LIMIT(10);

-- OR 

SELECT 
	CAST(lpep_pickup_datetime AS date) as pu_date,
	MAX(trip_distance) as max_trip_dist
	
FROM 
	green_taxi_trips
GROUP BY CAST(lpep_pickup_datetime AS date)	
ORDER BY max_trip_dist DESC
LIMIT(10);

```


## Question 5. The number of passengers

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 
- "Brooklyn" "Manhattan" "Queens"
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" **THIS ONE**
- "Brooklyn" "Queens" "Staten Island"

```sql 
SELECT 
	CAST(g.lpep_pickup_datetime AS date) as pu_date,
	z."Borough",
	SUM(g.total_amount) AS total_amount_borough
	
FROM 
	green_taxi_trips g 
	JOIN zones z
		ON g."PULocationID" = z."LocationID"
WHERE g.total_amount IS NOT NULL
	AND CAST(lpep_pickup_datetime AS date) = '2019-09-18'
GROUP BY z."Borough", CAST(lpep_pickup_datetime AS date)
ORDER BY total_amount_borough DESC
LIMIT(10);
```

## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- JFK Airport   ** THIS ONE - tip of 62 on 103... they got to the airport in 34 minutes at 6pm on a friday. I am assuming that it was a close call.**  
- Long Island City/Queens Plaza

```sql
SELECT 
	CAST(g.lpep_pickup_datetime AS date) as pu_date,
	CAST(g.lpep_pickup_datetime AS time) as pickup_time,
	CAST(g.lpep_dropoff_datetime AS time) as dropoff_time,
	CAST(g.lpep_dropoff_datetime AS time) - CAST(g.lpep_pickup_datetime AS time) as trip_duration,
	z_pu."Zone" as pickup_zone,
	z_do."Zone" as dropoff_zone, 
	g.tip_amount,
	g.total_amount

FROM 
	green_taxi_trips g 
	JOIN zones z_pu
		ON g."PULocationID" = z_pu."LocationID"
	JOIN zones z_do
		ON g."DOLocationID" = z_do."LocationID"
WHERE z_pu."Zone" = 'Astoria'
ORDER BY tip_amount DESC
LIMIT(10);

```

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.
```cli
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.taxi-dataset will be created
  + resource "google_bigquery_dataset" "taxi-dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "taxi_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "EU"
      + max_time_travel_hours      = (known after apply)
      + project                    = "aerobic-badge-408610"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.taxi-bucket will be created
  + resource "google_storage_bucket" "taxi-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "EU"
      + name                        = "aerobic-badge-408610-taxi-bucket"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + rpo                         = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.taxi-dataset: Creating...
google_storage_bucket.taxi-bucket: Creating...
google_storage_bucket.taxi-bucket: Creation complete after 2s [id=aerobic-badge-408610-taxi-bucket]
google_bigquery_dataset.taxi-dataset: Creation complete after 2s [id=projects/aerobic-badge-408610/datasets/taxi_dataset]

```

## Submitting the solutions

* Form for submitting: 
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: