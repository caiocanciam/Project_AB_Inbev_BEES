from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# ------------------------------
# Gold Layer: Aggregated data for analytics
# ------------------------------
def gold_layer():
    spark = SparkSession.builder \
        .appName("gold_layer") \
        .config("spark.driver.bindAddress", "0.0.0.0") \
        .getOrCreate()


    input_url = "/opt/airflow/layers/silver/"
    output_path = "/opt/airflow/layers/gold/"

    # Read from silver layer
    df_input = spark.read.option("mergeSchema", "true").parquet(input_url)
    
    # Ensure location column is filled
    df_gold = df_input.withColumn(
        "brewery_location",
        F.coalesce(F.col("state"), F.col("state_province"))
    )
    
    # Remove duplicates
    df_gold = df_gold.dropDuplicates(["id"])
    
    # Aggregate brewery count per location and type
    df_gold = (
        df_gold.groupBy("brewery_location", "brewery_type")
          .agg(F.countDistinct("id").alias("brewery_count"))
          .orderBy("brewery_location", F.desc("brewery_count"))
    )
    
    # Save gold layer, partitioned by location
    df_gold.write \
        .mode("overwrite") \
        .partitionBy("brewery_location") \
        .parquet(output_path)
    