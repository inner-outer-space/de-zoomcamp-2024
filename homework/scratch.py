StructType([StructField('dispatching_base_num', StringType(), True), 
            StructField('pickup_datetime', StringType(), True), 
            StructField('dropOff_datetime', StringType(), True), 
            StructField('PUlocationID', DoubleType(), True), 
            StructField('DOlocationID', DoubleType(), True), 
            StructField('SR_Flag', DoubleType(), True), 
            StructField('Affiliated_base_number', StringType(), True)
])


schema = types.StructType([
    types.StructField('dispatching_base_num', types.StringType(), True), 
    types.StructField('pickup_datetime', types.TimestampType(), True), 
    types.StructField('dropOff_datetime', types.TimestampType(), True), 
    types.StructField('PUlocationID', types.IntegerType(), True), 
    types.StructField('DOlocationID', types.IntegerType(), True), 
    types.StructField('SR_Flag', types.DoubleType(), True), 
    types.StructField('Affiliated_base_number', types.StringType(), True)
])
           

schema = types.StructType([
    types.StructField('hvfhs_license_num', types.StringType(), True),
    types.StructField('dispatching_base_num', types.StringType(), True), 
    types.StructField('pickup_datetime', types.TimestampType(), True), 
    types.StructField('dropoff_datetime',types.TimestampType(), True), 
    types.StructField('PULocationID', types.IntegerType(), True), 
    types.StructField('DOLocationID', types.IntegerType(), True), 
    types.StructField('SR_Flag', types.StringType(), True)
])