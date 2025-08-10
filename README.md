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

# Monitoring and Alerting
To ensure the pipeline’s reliability and visibility, I would adopt a monitoring and alerting strategy in three layers:

1. Pipeline Monitoring (Airflow)
- Execution metrics: Use Airflow’s native UI to track task duration, retry attempts, and success/failure status.
- Failure alerts: Configure email notifications or integrate with Slack/MS Teams to notify when a DAG or task fails.
- Automatic retries: Already implemented in the DAG (2 attempts with delay between them), minimizing temporary failures such as API unavailability.

2. Data Quality Monitoring
- Validations in Silver and Gold layers:
  - Check processed volumes and compare against historical averages.
  - Ensure critical columns (id, state, brewery_type) have no null or invalid values.
  - Validate partitioning consistency by state.
  - Action on failure: Stop the pipeline if critical checks fail, preventing invalid data from propagating to the Gold layer.
- Suggestion:
  - Create additional tasks in the DAG to run quality checks using Great Expectations or PySpark/Pandas scripts (data reports) before proceeding to the next layers.

3. Observability and Logging
- Structured logs: Leverage Airflow logs with clear messages on start, end, and any errors in each step.
- Log storage: Persist logs on durable volumes or send them to a centralized logging service (e.g., CloudWatch, Grafana) for historical review.
- Dashboards: Use Grafana to visualize metrics such as average execution time, number of failures, and volume of data processed per day.

# Incidents Alert Workflow
- Failure is logged in Airflow.
- An automatic alert is sent (email).
- The data team receives the notification and accesses Airflow logs to identify the root cause.
- If the issue is data-related (e.g., API returning an empty list), apply manual reprocessing logic (through an Airflow environment variable) or adjust the code.
