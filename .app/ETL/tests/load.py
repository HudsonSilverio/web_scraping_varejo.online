import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import os
from dotenv import load_dotenv

import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do banco de dados
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)

def criando_conexao():
    """Cria uma conexão com o banco de dados PostgreSQL."""
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    return conn

def configuracao_df(conn):
    """Cria a tabela de preços se ela não existir."""
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

def save_to_database(data, table_name='tv.prices'):
    """Salva os dados no banco de dados."""
    df = pd.DataFrame([data])
    df.to_sql(table_name, engine, if_exists='append', index=False)

def get_max_price(conn):
    """Consulta o maior preço registrado até o momento."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT preco_atual, timestamp 
        FROM tv.prices 
        WHERE preco_atual = (SELECT MAX(preco_atual) FROM tv.prices);
    """)
    result = cursor.fetchone()
    cursor.close()
    return result if result else (None, None)
