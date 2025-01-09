# poetry run python main.py

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


load_dotenv()

# Configurações do bot do Telegram
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
bot = Bot(token=TOKEN)

# Configurações do banco de dados PostgreSQL
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# Cria o engine do SQLAlchemy para o PostgreSQL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)

def pag_produto(): # Essa função será usada para acessar a página da web e obter seu conteúdo (o HTML da página). 
    url = "https://www.amazon.com.br/Samsung-Smart-Crystal-UHD-55DU8000/dp/B0CYN9P8TS/ref=sr_1_3?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dib=eyJ2IjoiMSJ9.ejoQJGWcp6_aW17EYE8TQo9GepQubyQjmd9POOyKWJrKBdrDpBTDHbKn1suasUCAb1fKUlNbmrmMBlTZ9qYk0oXqX9GUdHZPOpQ9800Fm6qDG99srlQIH79K3QW7GDYZM-qLkxxkHqajqYGWNzOgE1GdtIDXN0pN-BSXxWLQp3Zjs0TXEg7pfTIFNxWdJordPpWZtNffeuHEAUOCl-_Rv8lNPeX1Kau67NHg6KP6t8j7vS1ukGMFSXgQYaGaFFIuwQDzdIVJPoUo5mNjy2cbE06k9CTDPJmUQPs6f2rOqAM.Kq3Amm7LmNy51uf2ofTa4Kcc9QNGUqW0M7vkh0h6zJc&dib_tag=se&keywords=televisao+sansung+DU&qid=1735850371&sr=8-3&ufe=app_do%3Aamzn1.fos.25548f35-0de7-44b3-b28e-0f56f3f96147"
    response = requests.get(url)
    return response.text

def parse_page(html): # funcao que coleta exatamente a parte que voce deseja do HTML
    soup = BeautifulSoup(html, 'html.parser')
    preco_antigo = soup.find('span', class_='a-offscreen').get_text().replace('R$', ' ')
    nome_produto = soup.find('span',id="productTitle", class_='a-size-large product-title-word-break').get_text().replace(' ', '')
   
    categoria_1: list = soup.find_all('span', class_='a-price-whole')
    preco_atual = categoria_1[-2].get_text()  # Coleta o texto diretamente

    categoria_2: list = soup.find_all('span', class_='a-offscreen')
    preco_antigo = categoria_2[0].get_text()  # Coleta o texto diretamente

    # Limpeza e conversão para float
    preco_atual = float(preco_atual.replace('.', '').replace(',', '.'))
    preco_antigo = float(preco_antigo.replace('R$', '').replace('.', '').replace(',', '.'))

    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S') # cod para marcar a hora da coleta
    
    return {
        'nome_produto': nome_produto,
        'preco_atual' : preco_atual,
        'preco_antigo': preco_antigo,
        'timestamp' : timestamp
    }

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
        CREATE TABLE IF NOT EXISTS prices (
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

def save_to_database(data, table_name='prices'):
    """Salva uma linha de dados no banco de dados PostgreSQL usando pandas e SQLAlchemy."""
    df = pd.DataFrame([data])
    # Usa SQLAlchemy para salvar os dados no PostgreSQL
    df.to_sql(table_name, engine, if_exists='append', index=False)

def get_max_price(conn):
    """Consulta o maior preço registrado até o momento com o timestamp correspondente."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT preco_atual, timestamp 
        FROM prices 
        WHERE preco_atual = (SELECT MAX(preco_atual) FROM prices);
    """)
    result = cursor.fetchone()
    cursor.close()
    if result and result[0] is not None:
        return result[0], result[1]
    return None, None

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
