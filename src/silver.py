import pandas as pd
import duckdb
import re
import os
from dotenv import load_dotenv

load_dotenv()

account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")

container_bronze = "bronze"
file_bronze = "inscricoes.csv"
storage_options = {'account_name': account_name, 'account_key': account_key}

azure_path = f"az://{container_bronze}/{file_bronze}"

df = pd.read_csv(
    azure_path,
    storage_options = storage_options
)

df["email"] = df["email"].str.strip().str.lower()

df["cidade"] = df["cidade"].str.strip().str.title()

df["data_cadastro"] = pd.to_datetime(
    df["data_cadastro"]
).dt.date

container_silver = "silver"
file_silver = "inscricoes_limpas.parquet"
path_silver = f"az://{container_silver}/{file_silver}"

try:
    print("Iniciando a gravação dos dados na Silver")

    df.to_parquet(
        path_silver,
        storage_options = storage_options,
        index = False
    )

    print("✅ Dados gravados com sucesso na camada Silver!")
except:
    print("❌ Gravação de dados na Silver falhou!")


