from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
}

dag = DAG(
    'example_dag', 
    default_args=default_args, 
    schedule=None
)

task = EmptyOperator(
    task_id='dummy_task',
    dag=dag
)
