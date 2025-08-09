import sqlite3
import os
import glob
import pandas as pd


# ------------------------------
# Save Gold Layer into SQLite DB
# ------------------------------
def save_to_db():
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
