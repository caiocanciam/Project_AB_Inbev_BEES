# Descrição
Este projeto consiste em extrair dados de cervejarias dos EUA e da Irlanda utilizando a Breweries API, processando-os por meio de uma Arquitetura Medalhão (Bronze, Silver, Gold) e orquestrando todo o fluxo de trabalho com Apache Airflow.\

O objetivo é gerar visões agregadas sobre a quantidade de cervejarias por tipo e localização, armazenando os resultados em um banco de dados SQLite e validando-os via DBeaver.

# Arquitetura do Projeto
<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/509a1a6c-ac64-4de7-831d-9320cbb0638b" />

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
- DBeaver (opcional, para visualização dos dados após o processamento).

# Etapas
1. Configuração do Ambiente com Docker:
   - Iniciar containers do Apache Airflow e Jupyter Notebook para orquestrar e desenvolver o processo ETL.
<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/4b2834a3-7d25-4cba-83f9-fda85562aded" />
<img width="1200" height="500" alt="image" src="https://github.com/user-attachments/assets/ac3b4120-ee8b-492b-9431-f4f8aa75c233" />

2. Camada Bronze:
   - Extrair dados brutos de cervejarias a partir da API e armazenar no formato Parquet.
   - # COLOCAR UMA IMAGEM
  
   - 
3. Camada Silver:
   - Limpar, normalizar e remover duplicatas; adicionar campos de localização e datas de processamento.
   - # COLOCAR UMA IMAGEM
  
   
4. Camada Gold:
   - Agregar a contagem de cervejarias por tipo e localização.
  - # COLOCAR UMA IMAGEM
  
5. Carga no Banco de Dados:
   - Salvar o dataset final agregado em um banco SQLite.
  - # COLOCAR UMA IMAGEM

7. Validação no DBeaver:
   - Conectar ao banco SQLite e explorar os resultados de forma interativa.
  - # COLOCAR UMA IMAGEM
