# Description
This project consists of extracting brewery data using the Breweries API, processing it through a Medallion Architecture (Bronze, Silver, Gold), and orchestrating the entire workflow using Apache Airflow.

The goal is to generate aggregated views on the number of breweries by type and location, storing the results in a SQLite database and validating them via DBeaver.

# Project Architecture
<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/d0797a5f-743f-4d1f-ad81-08fe0d7b2620" />

# Medallion Architecture
- Bronze Layer: Raw data extraction from the API and storage in Json format.
- Silver Layer: Data cleaning, structuring for analysis, adding control columns.
- Gold Layer: Data aggregation for high-level insights, grouped by brewery type and location.

# Technologies Used
- Local Cluster: Used for data processing with PySpark. (Simulates a real big data environment and could be easily replaced by AWS EMR or Databricks.)
- Docker: Containerized environment to run Apache Airflow and Jupyter Notebook locally for development.
- Apache Airflow: Workflow orchestration tool to schedule and manage ETL pipelines.
- PySpark: Distributed data processing engine for transformations across Bronze, Silver, and Gold layers.
- Breweries API: Public API providing brewery details.
- DBeaver: Database tool for visually inspecting the processed SQLite database.

# Prerequisites
- Docker installed and configured.
- Python 3.x with PySpark and Airflow dependencies.
- DBeaver for data visualization after processing.

# Steps
1. Docker Environment Setup:
   - Launch Apache Airflow and Jupyter Notebook containers for orchestrating and developing the ETL process.

<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/4b2834a3-7d25-4cba-83f9-fda85562aded" />\
<img width="1200" height="500" alt="image" src="https://github.com/user-attachments/assets/ac3b4120-ee8b-492b-9431-f4f8aa75c233" />

2. Bronze Layer:
   - Extract raw brewery data from the API and store it in Json format.
<img width="726" height="249" alt="image" src="https://github.com/user-attachments/assets/079d6ed7-8090-4328-81e2-80b38b78e873" />

3. Silver Layer:
   - Clean, normalize, and deduplicate data; add location fields and processing dates, and save in Parquet format.
<img width="600" height="500" alt="image" src="https://github.com/user-attachments/assets/a4d815e1-0cbb-4895-9004-6ee6b8296d1a" />

4. Gold Layer:
   - Aggregate brewery counts by type and location.
<img width="600" height="540" alt="image" src="https://github.com/user-attachments/assets/034fd23b-ff35-4a22-b085-d7e7ce687ee8" />

5. Database Load:
   - Save the final aggregated dataset into a SQLite database.
<img width="721" height="258" alt="image" src="https://github.com/user-attachments/assets/c1bf317a-84e6-4cb8-b951-8e0c8d0e1a0d" />

7. Validation in DBeaver:
   - Connect to the SQLite database and explore the results interactively.
<img width="500" height="600" alt="image" src="https://github.com/user-attachments/assets/cd3b634a-27e9-465f-993c-22bb8e6089f9" />
