
import os
from typing import Optional, Tuple

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import create_engine

# Carregar as variáveis do arquivo .env
load_dotenv()

# Configurações do banco de dados
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)

# Modelo Pydantic para validação dos dados de preços
class PrecoProduto(BaseModel):
    product_name: str
    preco_atual: float
    preco_antigo: Optional[float]
    timestamp: str

    @field_validator('product_name')
    def validar_nome_produto(cls, v):
        if not v.strip():
            raise ValueError('O nome do produto não pode ser vazio ou apenas espaços.')
        return v

    @field_validator('preco_atual')
    def validar_preco_atual(cls, v):
        if v <= 0:
            raise ValueError('O preço atual deve ser maior que zero.')
        return v

    @field_validator('preco_antigo')
    def validar_preco_antigo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('O preço antigo, se presente, deve ser maior que zero.')
        return v

# Função para criar a conexão com o banco de dados
def criando_conexao():
    """Cria uma conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise

# Função para criar a tabela de preços, caso não exista
def configuracao_df(conn):
    """Cria a tabela de preços se ela não existir."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tv.prices (
                id SERIAL PRIMARY KEY,
                product_name TEXT,
                preco_atual FLOAT,
                preco_antigo FLOAT,
                timestamp TIMESTAMP
            )
        ''')
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Erro ao configurar a tabela: {e}")
        conn.rollback()
        raise

# Função para salvar os dados no banco de dados
def save_to_database(data, table_name='tv.prices'):
    """Salva os dados no banco de dados."""
    try:
        df = pd.DataFrame([data])
        df.to_sql(table_name, engine, if_exists='append', index=False)
    except Exception as e:
        print(f"Erro ao salvar os dados no banco de dados: {e}")
        raise

# Função para consultar o maior preço registrado até o momento
def get_max_price(conn) -> Tuple[Optional[float], Optional[str]]:
    """Consulta o maior preço registrado até o momento."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT preco_atual, timestamp 
            FROM tv.prices 
            WHERE preco_atual = (SELECT MAX(preco_atual) FROM tv.prices);
        """)
        result = cursor.fetchone()
        cursor.close()
        return result if result else (None, None)
    except Exception as e:
        print(f"Erro ao consultar o maior preço: {e}")
        return None, None


#___________________________________________

# import os
# from typing import Optional, Tuple

# import pandas as pd
# import psycopg2
# from dotenv import load_dotenv
# from pydantic import BaseModel, Field, field_validator
# from sqlalchemy import create_engine

# load_dotenv()

# # Configurações do banco de dados
# POSTGRES_DB = os.getenv("POSTGRES_DB")
# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT")
# DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
# engine = create_engine(DATABASE_URL)

# # Modelo Pydantic para validação dos dados de preços
# class PrecoProduto(BaseModel):
#     product_name: str
#     preco_atual: float
#     preco_antigo: Optional[float]
#     timestamp: str

#     # Usando o @field_validator para Pydantic V2
#     @field_validator('product_name')
#     def validar_nome_produto(cls, v):
#         if not v.strip():
#             raise ValueError('O nome do produto não pode ser vazio ou apenas espaços.')
#         return v

#     @field_validator('preco_atual')
#     def validar_preco_atual(cls, v):
#         if v <= 0:
#             raise ValueError('O preço atual deve ser maior que zero.')
#         return v

#     @field_validator('preco_antigo')
#     def validar_preco_antigo(cls, v):
#         if v is not None and v <= 0:
#             raise ValueError('O preço antigo, se presente, deve ser maior que zero.')
#         return v

# # Função para criar a conexão com o banco de dados
# def criando_conexao():
#     """Cria uma conexão com o banco de dados PostgreSQL."""
#     try:
#         conn = psycopg2.connect(
#             dbname=POSTGRES_DB,
#             user=POSTGRES_USER,
#             password=POSTGRES_PASSWORD,
#             host=POSTGRES_HOST,
#             port=POSTGRES_PORT
#         )
#         return conn
#     except Exception as e:
#         print(f"Erro ao conectar ao banco de dados: {e}")
#         raise

# # Função para criar a tabela de preços, caso não exista
# def configuracao_df(conn):
#     """Cria a tabela de preços se ela não existir."""
#     try:
#         cursor = conn.cursor()
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS tv.prices (
#                 id SERIAL PRIMARY KEY,
#                 product_name TEXT,
#                 preco_atual FLOAT,
#                 preco_antigo FLOAT,
#                 timestamp TIMESTAMP
#             )
#         ''')
#         conn.commit()
#         cursor.close()
#     except Exception as e:
#         print(f"Erro ao configurar a tabela: {e}")
#         conn.rollback()
#         raise

# # Função para salvar os dados no banco de dados
# def save_to_database(data, table_name='tv.prices'):
#     """Salva os dados no banco de dados."""
#     try:
#         df = pd.DataFrame([data])
#         df.to_sql(table_name, engine, if_exists='append', index=False)
#     except Exception as e:
#         print(f"Erro ao salvar os dados no banco de dados: {e}")
#         raise

# # Função para consultar o maior preço registrado até o momento
# def get_max_price(conn) -> Tuple[Optional[float], Optional[str]]:
#     """Consulta o maior preço registrado até o momento."""
#     try:
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT preco_atual, timestamp 
#             FROM tv.prices 
#             WHERE preco_atual = (SELECT MAX(preco_atual) FROM tv.prices);
#         """)
#         result = cursor.fetchone()
#         cursor.close()
#         return result if result else (None, None)
#     except Exception as e:
#         print(f"Erro ao consultar o maior preço: {e}")
#         return None, None



#_______________________________________________________________

# import pandas as pd
# from sqlalchemy import create_engine
# import psycopg2
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Configurações do banco de dados
# POSTGRES_DB = os.getenv("POSTGRES_DB")
# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT")
# DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
# engine = create_engine(DATABASE_URL)

# def criando_conexao():
#     """Cria uma conexão com o banco de dados PostgreSQL."""
#     conn = psycopg2.connect(
#         dbname=POSTGRES_DB,
#         user=POSTGRES_USER,
#         password=POSTGRES_PASSWORD,
#         host=POSTGRES_HOST,
#         port=POSTGRES_PORT
#     )
#     return conn

# def configuracao_df(conn):
#     """Cria a tabela de preços se ela não existir."""
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS tv.prices (
#             id SERIAL PRIMARY KEY,
#             product_name TEXT,
#             preco_atual FLOAT,
#             preco_antigo FLOAT,
#             timestamp TIMESTAMP
#         )
#     ''')
#     conn.commit()
#     cursor.close()

# def save_to_database(data, table_name='tv.prices'):
#     """Salva os dados no banco de dados."""
#     df = pd.DataFrame([data])
#     df.to_sql(table_name, engine, if_exists='append', index=False)

# def get_max_price(conn):
#     """Consulta o maior preço registrado até o momento."""
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT preco_atual, timestamp 
#         FROM tv.prices 
#         WHERE preco_atual = (SELECT MAX(preco_atual) FROM tv.prices);
#     """)
#     result = cursor.fetchone()
#     cursor.close()
#     return result if result else (None, None)
