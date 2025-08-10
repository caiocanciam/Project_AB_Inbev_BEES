import pytz
import os
import json
import pandas as pd

from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col, coalesce


# ------------------------------
# Silver Layer: Data cleaning & standardization
# ------------------------------
def silver_layer():
    spark = SparkSession.builder \
    .appName("silver_layer") \
    .config("spark.driver.bindAddress", "0.0.0.0") \
    .getOrCreate()

    input_url = "/opt/airflow/layers/bronze/"
    output_path = "/opt/airflow/layers/silver/"
    
    todos_dados = []
    
    for arquivo in os.listdir(input_url):
        if arquivo.endswith(".json"): # Get only .json
            caminho = os.path.join(input_url, arquivo)
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
                todos_dados.append(dados)
    
    # Read raw data from bronze layer
    df_spark = spark.read.option("multiline", "true").json(input_url)
    
    # Force all columns to string for consistency
    df_spark = df_spark.select([F.col(c).cast("string").alias(c) for c in df_spark.columns])
    
    # Create location column (city or state_province)
    df_silver = df_spark.withColumn(
        "brewery_location",
        coalesce(col("state"), col("state_province"))
    )
    
    # Add execution date column
    date = str(datetime.now(pytz.timezone("Brazil/East"))).split(" ")[0]
    df_silver = df_silver.withColumn("exec_date", F.to_date(F.lit(date)))
    
    # Validation
    check_brewery_type = df_silver.where("brewery_type is NULL")
    check_brewery_location = df_silver.where("brewery_location is NULL")

    check_fail = []
    check_dict = {}

    if check_brewery_type.count() > 0:
        check_fail.append("brewery_type")
        check_dict["brewery_type"] = check_brewery_type.toPandas()
        check_dict["unique_brewery_type"] = (
            check_brewery_type.select("id").distinct().toPandas()
        )
    
    if check_brewery_location.count() > 0:
        check_fail.append("brewery_location")
        check_dict["brewery_location"] = check_brewery_location.toPandas()
        check_dict["unique_brewery_location"] = (
            check_brewery_location.select("id", "address_1", "address_2", "address_3", "city").distinct().toPandas()
        )

    if len(check_fail) > 0:
        local_folder_path = "/opt/airflow/layers/data_report/"
        file_name = "data_report.xlsx"
        os.makedirs(local_folder_path, exist_ok=True)

        full_path = os.path.join(local_folder_path, file_name)

        with pd.ExcelWriter(full_path, engine="openpyxl") as writer:
            for sheet_name, df in check_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        raise Exception(
            f"Validation failed for {', '.join(check_fail)}. Excel report generated at: {full_path}"
        )

    # Save silver layer, partitioned by location
    df_silver.write \
        .mode("overwrite") \
        .partitionBy("brewery_location") \
        .parquet(output_path)
    