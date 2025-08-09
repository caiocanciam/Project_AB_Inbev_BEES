from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import requests
import json

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ------------------------------
# Bronze Layer: Raw data ingestion
# ------------------------------
def bronze_layer():
    input_url = "https://api.openbrewerydb.org/v1/breweries"
    prefix = "/opt/airflow/layers/bronze"
    file_name = "breweries_list.json"
    output_path = os.path.join(prefix, file_name)
    
    # Retry strategy for API calls
    retry_strategy = Retry(
        total=2,
        backoff_factor=1,
        status_forcelist=[400, 401, 402, 403, 429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    try:
        response = session.get(input_url)
        response.raise_for_status()
        if response.status_code == 200:
            dados_json = response.json()
        else:
            error_message = f"Error accessing data: {response.status_code}"
            raise Exception(error_message)
    except Exception as e:
        error_message = f"Error processing JSON: {e}"
        raise Exception(error_message)
    
    conteudo_json = json.dumps(dados_json, indent=4, ensure_ascii=False)
    
    # Save raw JSON to bronze layer
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(conteudo_json)
    except Exception as e:
        print(f"Error saving file: {e}")
        
# ------------------------------
# Silver Layer: Data cleaning & standardization
# ------------------------------
def silver_layer():
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F
    from pyspark.sql.functions import col, coalesce
    import pytz

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
        coalesce(col("city"), col("state_province"))
    )
    
    # Remove duplicates by brewery ID
    df_silver = df_silver.dropDuplicates(["id"])
    
    # Add execution date column
    date = str(datetime.now(pytz.timezone("Brazil/East"))).split(" ")[0]
    df_silver = df_silver.withColumn("exec_date", F.to_date(F.lit(date)))
    
    # Save silver layer, partitioned by location
    df_silver.write \
        .mode("overwrite") \
        .partitionBy("brewery_location") \
        .parquet(output_path)


# ------------------------------
# Gold Layer: Aggregated data for analytics
# ------------------------------
def gold_layer():
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F

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
        F.coalesce(F.col("city"), F.col("state_province"), F.col("state"))
    )
    
    # Fill missing values
    df_gold = df_gold.fillna({"brewery_location": "UNKNOWN", "brewery_type": "UNKNOWN"})
    
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


# ------------------------------
# Save Gold Layer into SQLite DB
# ------------------------------
def save_to_db():
    import sqlite3
    import os
    import glob
    import pandas as pd
    
    input_path = '/opt/airflow/layers/gold/'
    db_path = '/opt/airflow/layers/database/meu_banco.db'
    table_name = 'breweries_list'

    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Path {input_path} not found.")

        parquet_files = glob.glob(os.path.join(input_path, '**', '*.parquet'), recursive=True)

        if not parquet_files:
            raise FileNotFoundError("No .parquet file found.")

        print(f"Found {len(parquet_files)} parquet files.")

        df_list = []
        for file in parquet_files:
            # Extract only location name from partition folder
            location = os.path.basename(os.path.dirname(file)).split("=", 1)[1]
            df_temp = pd.read_parquet(file)
            df_temp['brewery_location'] = location
            df_list.append(df_temp)

        # Combine all partitions into one DataFrame
        df = pd.concat(df_list, ignore_index=True)

        # Save to SQLite
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()

        print(f"Data saved to SQLite successfully.")
    except Exception as e:
        print(f"Error saving to database: {e}")


# ------------------------------
# Airflow DAG definition
# ------------------------------
with DAG(
    dag_id='ETL_Pipeline_Breweries',
    start_date=datetime(2025, 8, 7),
    schedule_interval=None,
    catchup=False,
) as dag:
    bronze = PythonOperator(task_id='bronze_breweries', python_callable=bronze_layer)
    silver = PythonOperator(task_id='silver_breweries', python_callable=silver_layer)
    gold = PythonOperator(task_id='gold_breweries', python_callable=gold_layer)
    table = PythonOperator(task_id='save_to_db', python_callable=save_to_db)

    bronze >> silver >> gold >> table