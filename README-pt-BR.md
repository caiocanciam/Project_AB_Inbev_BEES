# Descrição
Este projeto consiste em extrair dados de cervejarias utilizando a Breweries API, processando-os por meio de uma Arquitetura Medalhão (Bronze, Silver, Gold) e orquestrando todo o fluxo de trabalho com Apache Airflow.

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
<img width="600" height="500" alt="image" src="https://github.com/user-attachments/assets/a4d815e1-0cbb-4895-9004-6ee6b8296d1a" />

4. Camada Gold:
   - Agregar a contagem de cervejarias por tipo e localização.
<img width="600" height="540" alt="image" src="https://github.com/user-attachments/assets/034fd23b-ff35-4a22-b085-d7e7ce687ee8" />

5. Carga no Banco de Dados:
   - Salvar o dataset final agregado em um banco SQLite.
<img width="721" height="258" alt="image" src="https://github.com/user-attachments/assets/c1bf317a-84e6-4cb8-b951-8e0c8d0e1a0d" />

7. Validação no DBeaver:
   - Conectar ao banco SQLite e explorar os resultados de forma interativa.
<img width="500" height="600" alt="image" src="https://github.com/user-attachments/assets/cd3b634a-27e9-465f-993c-22bb8e6089f9" />

# Monitoramento e Alertas
Para garantir a confiabilidade e a visibilidade do pipeline, adotaria uma estratégia de monitoramento e alertas em três níveis:

1. Monitoramento de Pipeline (Airflow)
- Métricas de execução: Utilizar o painel nativo do Airflow para acompanhar duração das tarefas, tentativas de reexecução e status de sucesso/falha.
- Alertas por falha: Configuração de e-mails ou integração com Slack/MS Teams para notificar quando uma DAG ou tarefa falhar.
- Retries automáticos: Já implementados no DAG (2 tentativas com intervalo entre elas), minimizando falhas temporárias como indisponibilidade da API.

2. Monitoramento de Qualidade de Dados
- Validações no Silver e Gold:
  - Checagem de volumes processados e comparação com médias históricas.
  - Conferir se colunas críticas (id, state, brewery_type) não contêm valores nulos ou inválidos.
  - Validar consistência no particionamento por estado.
  - Interromper o pipeline caso os checks críticos falhem, evitando propagação de dados inválidos para a camada gold.
- Sugestão:
  - Criar tarefas extras no DAG que executem testes de qualidade usando Great Expectations ou scripts PySpark/Pandas (data reports) antes de prosseguir para as próximas camadas.

3. Observabilidade e Logging
- Logs estruturados: Aproveitar os logs do Airflow, com mensagens claras sobre início, fim e possíveis erros de cada etapa.
- Armazenamento de logs: Salvar logs em volumes persistentes ou enviar para um serviço de log centralizado (ex.: CloudWatch, Grafana) para consulta histórica.
- Dashboards: Utilizar Grafana para visualizar métricas como tempo médio de execução, número de falhas e volume de dados processados por dia.

4. Fluxo de Alerta em Caso de Problema
- Falha é registrada no Airflow.
- Alerta é enviado automaticamente (e-mail).
- Equipe de dados recebe notificação e acessa logs no Airflow para identificar a causa.
- Se o problema for de dados (ex.: API retornando lista vazia), aplicar lógica de reprocessamento manual (em variável de ambiente no Airflow) ou ajuste de código.
