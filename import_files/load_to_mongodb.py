from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType
import os
from pathlib import Path

# Initialize Spark Session with MongoDB connector
spark = SparkSession.builder \
    .appName("CSV to MongoDB ETL") \
    .config("spark.mongodb.output.uri", "mongodb://mongo:27017/") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .getOrCreate()

# Define a UDF for encoding string columns
# def utf8_encode(value):
#     if value:
#         return value.encode("ISO-8859-1").decode("utf-8")
#     return None

# utf8_encode_udf = udf(utf8_encode, StringType())

def process_file(file_path):
    # Get the filename without extension
    filename = Path(file_path).stem

    # Determine the collection name based on the filename
    collection_name = None
    if 'Nota' in filename:
        collection_name = 'notas_fiscais'
    elif 'Emenda' in filename:
        collection_name = 'emenda'
    elif 'Despesas' in filename:
        collection_name = 'despesas'
    else:
        print(f"Skipping file {filename} as it doesn't match any collection pattern")
        return

    try:
        # Read CSV with ISO-8859-1 encoding
        df = spark.read \
            .option("encoding", "ISO-8859-1") \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv(file_path)

        # # Convert the encoding to UTF-8 for all string columns
        # for column in df.columns:
        #     print(column)
        #     if df.schema[column].dataType.simpleString() == 'string':
        #         df = df.withColumn(
        #             column,
        #             df[column].cast('string').encode('utf-8')
        #         )


        # Convert the encoding to UTF-8 for all string columns using the UDF
        # for column in df.columns:
        #     if df.schema[column].dataType.simpleString() == 'string':
        #         df = df.withColumn(column, utf8_encode_udf(col(column)))

        # Write to MongoDB
        df.write \
            .format("mongo") \
            .mode("append") \
            .option("database", "gastospublicos") \
            .option("collection", collection_name) \
            .save()

        print(f"Successfully processed {filename} into collection {collection_name}")

    except Exception as e:
        print(f"Error processing file {filename}: {str(e)}")

def main():
    # Path to the data folder
    data_folder = "data"

    # Get all CSV files from the data folder
    csv_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder)
                if f.lower().endswith('.csv')]

    if not csv_files:
        print("No CSV files found in the data folder")
        return

    # Process each file
    for file_path in csv_files:
        process_file(file_path)

    print("ETL process completed")
    spark.stop()

if __name__ == "__main__":
    main()
