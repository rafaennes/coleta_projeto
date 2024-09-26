from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace, to_timestamp
from pyspark.sql.types import FloatType, TimestampType

# Create a SparkSession
spark = SparkSession.builder \
    .appName("MongoDB ETL") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/gastospublicos.notasfiscais") \ 
    .config("spark.mongodb.output.uri", "mongodb://<your_connection_string>/gastospublicos.slv_notasfiscais") \
    .getOrCreate()

# Read data from MongoDB
df = spark.read.format("mongo").load()

# Replace commas with periods and convert to float
df = df.withColumn("float_column", regexp_replace(col("original_column"), ",", ".").cast(FloatType()))

# Convert to timestamp (adjust the format as needed)
df = df.withColumn("timestamp_column", to_timestamp(col("original_timestamp_column"), "<your_timestamp_format>"))

# Write the transformed data back to MongoDB (or another destination)
df.write.format("mongo").mode("overwrite").save() 