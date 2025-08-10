from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Import ETL tasks
from tasks.bronze_layer import bronze_layer
from tasks.silver_layer import silver_layer
from tasks.gold_layer import gold_layer
from tasks.save_to_db import save_to_db


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
