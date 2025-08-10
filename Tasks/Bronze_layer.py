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
