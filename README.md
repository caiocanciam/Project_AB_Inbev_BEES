# Descrição
This project consists of extracting brewery data from the USA and Ireland using the Breweries API, processing it through a Medallion Architecture (Bronze, Silver, Gold), and orchestrating the entire workflow using Apache Airflow.\

The goal is to generate aggregated insights on the number of breweries per type and location, storing the results in a SQLite database and validating them via DBeaver.

# Project Architecture
<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/509a1a6c-ac64-4de7-831d-9320cbb0638b" />



# Medallion Architecture
- Bronze Layer: Raw data extraction from the API and storage in Json format.
- Camada Silver: Data cleaning, structuring for analysis, adding control columns.
- Camada Gold: Data aggregation for high-level insights, grouped by brewery type and location.

# Technologies Used
- Local Cluster: Used for big data processing with PySpark. (Simulates a real big data environment and could be easily replaced by AWS EMR or Databricks.)
- Docker: Containerized environment to run Apache Airflow and Jupyter Notebook locally for development.
- Apache Airflow: Workflow orchestration tool to schedule and manage ETL pipelines.
- PySpark: Distributed data processing engine for transformations across Bronze, Silver, and Gold layers.
- Breweries API: Public API providing brewery details.
- DBeaver: Database tool for visually inspecting the processed SQLite database.

# Prerequisites
- Docker installed and configured.
- Python 3.x with PySpark and Airflow dependencies.
- DBeaver (optional, for data visualization after processing).

# Steps
1. Docker Environment Setup:
   - Launch Apache Airflow and Jupyter Notebook containers for orchestrating and developing the ETL process.
   - # COLOCAR UMA IMAGEM

2. Bronze Layer:
   - Extract raw brewery data from the API and store it in Parquet format.
   - # COLOCAR UMA IMAGEM
  
   - 
3. Silver Layer:
   - Clean, normalize, and deduplicate data; add location fields and processing dates.
   - # COLOCAR UMA IMAGEM
  
   
4. Gold Layer:
   - Aggregate brewery counts by type and location.
  - # COLOCAR UMA IMAGEM
  
5. Database Load:
   - Save the final aggregated dataset into a SQLite database.
  - # COLOCAR UMA IMAGEM

7. Validation in DBeaver:
   - Connect to the SQLite database and explore the results interactively.
  - # COLOCAR UMA IMAGEM

   - Criei Old_files para automatizar a exclusão de arquivos antigos na camada bronze assim que um novo for gerado.
