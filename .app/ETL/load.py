# import requests
# from bs4 import BeautifulSoup
# import time
# import sqlite3
# from sqlalchemy import create_engine
# import pandas as pd
# from extract import parse_page, pag_produto
# import os
# import asyncio

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine



# def criando_conexao(db_name='tv_sansung_prices.db'):
#     """Cria uma conexão com o banco de dados SQLite."""
#      # Define o caminho do banco de dados na pasta 'data'
#     #conn = sqlite3.connect(db_name)
#     conn = sqlite3.connect('./data/tv_sansung_prices.db')
#     return conn

# def configuracao_df(conn):
#     """Cria a tabela de preços se ela não existir."""
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS prices (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             product_name TEXT,
#             nome_produto INTEGER,
#             preco_atual INTEGER,
#             preco_antigo INTEGER,
#             timestamp TEXT
#         )
#     ''')
#     conn.commit()

# def save_to_database(conn, data):
#     """Salva uma linha de dados no banco de dados SQLite usando pandas."""
#     df = pd.DataFrame([data])  # Converte o dicionário em um DataFrame de uma linha
#     df.to_sql('prices', conn, if_exists='append', index=False)  # Salva no banco de dados

# def maximo_venda(conn): #funcao que conecta com o DB e retorna o preco maximo naquele momento
    
#     cursor = conn.cursor()
#     cursor.execute("SELECT MAX(preco_atual), timestamp FROM prices")
#     result = cursor.fetchone()
#     if result and result[0] is not None:
#         return result[0], result[1]
#     return None, None

# # Teste das funções
# if __name__ == '__main__':
#     # Configuração do banco de dados
#     conn = criando_conexao()
#     configuracao_df(conn)

#     while True:
#         # Faz a requisição e parseia a página
#         conteudo_pag = pag_produto()
#         coleta = parse_page(conteudo_pag)
#         current_price = coleta['preco_atual']
        
#         # Obtém o maior preço já salvo
#         max_price, max_price_timestamp = maximo_venda(conn)
        
#          # Comparação de preços
#         if max_price is None or current_price > max_price:
#             print(f"Preço maior detectado: {current_price}")
#             max_price = current_price  # Atualiza o maior preço
#             max_price_timestamp = coleta['timestamp']  # Atualiza o timestamp do maior preço
#         else:
#             print(f"O maior preço registrado é {max_price} em {max_price_timestamp}")
        
#         # Salva os dados no banco de dados SQLite
#         save_to_database(conn, coleta)
#         print("Dados salvos no banco:", coleta)
        
#         # Aguarda 10 segundos antes da próxima execução
#         time.sleep(10)

#     # Fecha a conexão com o banco de dados
#     conn.close()

# Configurações do banco de dados PostgreSQL
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# Cria o engine do SQLAlchemy para o PostgreSQL
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
            nome_produto INTEGER,
            preco_atual INTEGER,
            preco_antigo INTEGER,
            timestamp TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()

def save_to_database(data, table_name='tv.prices'):
    """Salva uma linha de dados no banco de dados PostgreSQL usando pandas e SQLAlchemy."""
    df = pd.DataFrame([data])
    # Usa SQLAlchemy para salvar os dados no PostgreSQL
    df.to_sql(table_name, engine, if_exists='append', index=False)
    
async def send_telegram_message(text):
    """Envia uma mensagem para o Telegram."""
    await bot.send_message(chat_id=CHAT_ID, text=text)

async def main():
    conn = criando_conexao()
    configuracao_df(conn)
    
    try:
            while True:
                # Faz a requisição e parseia a página
                page_content = pag_produto()
                product_info = parse_page(page_content)
                current_price = product_info['preco_atual']
                
                
                # Obtém o maior preço já salvo
                max_price, max_price_timestamp = get_max_price(conn)
                
                # Comparação de preços
                if max_price is None or current_price > max_price:
                    message = f"Novo preço maior detectado: {current_price}"
                    print(message)
                    await send_telegram_message(message)
                    max_price = current_price
                    max_price_timestamp = product_info['timestamp']
                else:
                    message = f"O maior preço registrado é {max_price} em {max_price_timestamp}"
                    print(message)
                    await send_telegram_message(message)

                # Salva os dados no banco de dados PostgreSQL
                save_to_database(product_info)
                print("Dados salvos no banco:", product_info)
                
                # Aguarda 10 segundos antes da próxima execução
                await asyncio.sleep(10)

    except KeyboardInterrupt:
            print("Parando a execução...")
    finally:
            conn.close()

# Executa o loop assíncrono
asyncio.run(main())
