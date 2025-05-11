


from pyspark.sql import SparkSession

from app.utils.transformations import (
    clean_missing,
    convert_age,
    simplify_readmitted,
    drop_irrelevant_cols
)
from dotenv import load_dotenv
from app.config import DATA_PATH, OUTPUT_PATH
import os

# Load environment variables
load_dotenv()
DATA_PATH = os.getenv("DATA_PATH", "data/diabetic_data.csv")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "output/")

def main():
    # Start Spark session
    spark = SparkSession.builder \
        .appName("HospitalReadmissionETL") \
        .getOrCreate()

    print("Reading data from:", DATA_PATH)
    df = spark.read.csv(DATA_PATH, header=True, inferSchema=True)

    print("Initial record count:", df.count())

    # Transform
    df = clean_missing(df)
    df = convert_age(df)
    df = simplify_readmitted(df)
    df = drop_irrelevant_cols(df)

    print("Transformed record count:", df.count())
    df.printSchema()

    # Write to output as Parquet
    output_file = os.path.join(OUTPUT_PATH, "cleaned_readmission_data.parquet")
    df_filtered.write.mode("overwrite").parquet(os.path.join(OUTPUT_PATH, "cleaned_data.parquet"))
    print("ETL job completed. Data written to:", output_file)

    spark.stop()

if __name__ == "__main__":
    main()



df = spark.read.csv(DATA_PATH, header=True, inferSchema=True)
...
df_filtered.write.mode("overwrite").parquet(OUTPUT_PATH + "cleaned_data.parquet")

