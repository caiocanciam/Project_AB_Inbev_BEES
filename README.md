# Descrição
Este projeto consiste em extrair dados sobre cervejarias nos EUA e Irlanda usando uma API como uma lista de cervejarias, processando-a em diferentes níveis (Bronze, Silver e Gold), usando Databricks e orquestrando o fluxo de dados com o Azure Data Factory. \

O objetivo é criar uma visualização com a quantidade de cervejarias por tipo e localização.

# Arquitetura do Projeto
<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/b3d66219-0328-4ff7-a4f2-1f026c43e1e4" />


# O projeto utiliza arquitetura medalhão:
- Camada Bronze: Extração de dados brutos em formato Parquet/Delta. \
- Camada Silver: Limpeza e estruturação de dados para análise, criação de comentários, criação de colunas de controle e otimização de tabelas. \
- Camada Gold: Agregação de dados para insights de alto nível, criação de comentários, criação de colunas de controle e otimização de tabelas.

# Tecnologias utilizadas
- Databricks: Para processamento e análise de dados usando PySpark. \
- Azure Data Factory: Para orquestração de fluxo de trabalho de dados. \
- Azure Key Vault: Para proteger o gerenciamento de chaves de recursos. \
- Breweries API: Fonte de dados sobre as cervejarias.

# Pré-requisitos
- Conta da Azure com acesso ao Databricks, Azure Data Factory e Azure Key Vault.

# Etapas
1. Criação de grupos de recursos:
   - Crie todos os grupos de recursos e recursos necessários para o desenvolvimento do projeto

2. Configuração do Azure Key Vault:
   - Armazene suas chaves no Azure Key Vault para dar acesso aos aplicativos.

3. Databricks:
   - Desenvolvimento de notebooks para o workspace Databricks aplicando extração, limpeza e agregação de dados. Como a ingestão de dados foi feita diretamente pelo Azure Data Factory e transformada em formato Parquet, os dados foram carregados na camada bronze e processados na camada silver e posteriormente na camada gold.
       - Silver_Breweries: 
       - Gold_Breweries:

4. Azure Data Factory:
   - Criação de Linked Service para acessar o Databricks, o DataLake Gen2 e a API:
  
   - Configure os pipelines para orquestrar a execução dos notebooks no Databricks na ordem Old_Files -> Copy_Data -> Silver -> Gold.
   - Criei Old_files para automatizar a exclusão de arquivos antigos na camada bronze assim que um novo for gerado.
