# poetry run python main.py

import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import pandas as pd
import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do bot do Telegram
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
bot = Bot(token=TOKEN)

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

    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S:') # cod para marcar a hora da coleta
    
    return {
        'nome_produto': nome_produto,
        'preco_atual' : preco_atual,
        'preco_antigo': preco_antigo,
        'timestamp' : timestamp
    }

def criando_conexao(db_name='tv_sansung_prices.db'):
    """Cria uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect('./data/tv_sansung_prices.db') #salvando o database 
    return conn

def configuracao_df(conn):
    """Cria a tabela de preços se ela não existir."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            nome_produto INTEGER,
            preco_atual INTEGER,
            preco_antigo INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()

def save_to_database(conn, data):
    """Salva uma linha de dados no banco de dados SQLite usando pandas."""
    df = pd.DataFrame([data])  # Converte o dicionário em um DataFrame de uma linha
    df.to_sql('prices', conn, if_exists='append', index=False)  # Salva no banco de dados

def maximo_venda(coon): #funcao que conecta com o DB e retorna o preco maximo naquele momento
    conn = sqlite3.connect('./data/tv_sansung_prices.db') #salvando o database 
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(preco_atual), timestamp FROM prices")
    result = cursor.fetchone()
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
            conteudo_pag = pag_produto()
            coleta = parse_page(conteudo_pag)
            current_price = coleta['preco_atual']
            
            # Obtém o maior preço já salvo
            max_price, max_price_timestamp = maximo_venda(conn)
            
            # Comparação de preços
            if max_price is None or current_price > max_price:
                message = f"Novo preço maior detectado: {current_price}"
                print(message)
                await send_telegram_message(message)
                max_price = current_price
                max_price_timestamp = coleta['timestamp']
            else:
                message = f"O maior preço registrado é {max_price} em {max_price_timestamp}"
                print(message)
                await send_telegram_message(message)

            # Salva os dados no banco de dados SQLite
            save_to_database(conn, coleta)
            print("Dados salvos no banco:", coleta)
            
            # Aguarda 10 segundos antes da próxima execução
            await asyncio.sleep(10)

    except KeyboardInterrupt:
        print("Parando a execução...")
    finally:
        conn.close()

# Executa o loop assíncrono
asyncio.run(main())
