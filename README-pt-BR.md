# Descrição
Este projeto consiste em extrair dados de cervejarias dos EUA e da Irlanda utilizando a Breweries API, processando-os por meio de uma Arquitetura Medalhão (Bronze, Silver, Gold) e orquestrando todo o fluxo de trabalho com Apache Airflow.

O objetivo é gerar visões agregadas sobre a quantidade de cervejarias por tipo e localização, armazenando os resultados em um banco de dados SQLite e validando-os via DBeaver.

# Arquitetura do Projeto
<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/d0797a5f-743f-4d1f-ad81-08fe0d7b2620" />

# Arquitetura Medalhão
- Camada Bronze: Extração de dados brutos da API e armazenamento no formato JSON.
- Camada Silver: Limpeza, estruturação para análise e adição de colunas de controle.
- Camada Gold: Agregação de dados para insights de alto nível, agrupados por tipo e localização de cervejarias.

# Tecnologias Utilizadas
- Cluster Local: Utilizado para processamento de big data com PySpark. (Simula um ambiente real de big data e pode ser facilmente substituído por AWS EMR ou Databricks.)
- Docker: Ambiente conteinerizado para executar Apache Airflow e Jupyter Notebook localmente para desenvolvimento.
- Apache Airflow: Ferramenta de orquestração de workflows para agendar e gerenciar pipelines ETL.
- PySpark: Motor de processamento distribuído para transformações nas camadas Bronze, Silver e Gold.
- Breweries API: API pública que fornece informações sobre cervejarias.
- DBeaver: Ferramenta para inspeção visual do banco de dados SQLite processado.

# Pré-requisitos
- Docker instalado e configurado.
- Python 3.x com dependências do PySpark e Airflow.
- DBeaver para visualização dos dados após o processamento.

# Etapas
1. Configuração do Ambiente com Docker:
   - Iniciar containers do Apache Airflow e Jupyter Notebook para orquestrar e desenvolver o processo ETL.

<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/4b2834a3-7d25-4cba-83f9-fda85562aded" />\
<img width="1200" height="500" alt="image" src="https://github.com/user-attachments/assets/ac3b4120-ee8b-492b-9431-f4f8aa75c233" />

2. Camada Bronze:
   - Extrair dados brutos de cervejarias a partir da API e armazenar no formato Json.
<img width="726" height="249" alt="image" src="https://github.com/user-attachments/assets/079d6ed7-8090-4328-81e2-80b38b78e873" />

3. Camada Silver:
   - Limpar, normalizar e remover duplicatas; adicionar campos de localização, datas de processamento e salvar em formato Parquet.
<img width="600" height="420" alt="image" src="https://github.com/user-attachments/assets/5e5031da-8647-42e2-b179-28f933efbfeb" />

4. Camada Gold:
   - Agregar a contagem de cervejarias por tipo e localização.
<img width="600" height="500" alt="image" src="https://github.com/user-attachments/assets/989eb30b-e6fa-4b2d-810d-c098ea96db9b" />

5. Carga no Banco de Dados:
   - Salvar o dataset final agregado em um banco SQLite.
<img width="721" height="258" alt="image" src="https://github.com/user-attachments/assets/c1bf317a-84e6-4cb8-b951-8e0c8d0e1a0d" />

7. Validação no DBeaver:
   - Conectar ao banco SQLite e explorar os resultados de forma interativa.
<img width="500" height="600" alt="image" src="https://github.com/user-attachments/assets/32228086-23fe-4ad7-a84d-5298b6754c41" />
