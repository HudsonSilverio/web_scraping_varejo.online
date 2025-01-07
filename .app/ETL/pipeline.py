# from .extract import parse_page, pag_produto
# from .load import criando_conexao, configuracao_df,save_to_database, maximo_venda
# from .transform import dataframe

# def pipeline_completa(url, html, coleta, df, conn, data, db_name):

import time
import sqlite3
import pandas as pd
from extract import pag_produto, parse_page
from transform import dataframe
from load import criando_conexao, configuracao_df, save_to_database, maximo_venda
from boot_code import send_message
import asyncio


TELEGRAM_TOKEN = "8068436836:AAGfDzr3J0ah6BQxrucG-Qt06uV9ANHXn1E"
TELEGRAM_CHAT_ID = "6816017490"

async def send_message():
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Teste de mensagem!")

# Executa a função assíncrona
asyncio.run(send_message())

def run_pipeline():
    # Cria a conexão com o banco de dados
    conn = criando_conexao()

    # Cria a tabela se não existir
    configuracao_df(conn)

    # Inicializa o dataframe
    df = pd.DataFrame()

    while True:
        # Extrai dados da página
        conteudo_pag = pag_produto()
        coleta = parse_page(conteudo_pag)

        # Transforma os dados e adiciona ao dataframe
        df = dataframe(coleta, df)

        # Salva os dados no banco de dados
        save_to_database(conn, coleta)
        print(f"Dados salvos no banco: {coleta}")

        # Verifica o preço máximo e envia uma mensagem no Telegram se necessário
        max_price, max_price_timestamp = maximo_venda(conn)
        current_price = coleta['preco_atual']

        if max_price is None or current_price > max_price:
            print(f"Novo preço maior detectado: {current_price}")
            max_price = current_price
            max_price_timestamp = coleta['timestamp']
            asyncio.run(send_message())  # Envia a mensagem para o Telegram

        # Aguarda 10 segundos antes de continuar o processo
        time.sleep(10)

    # Fecha a conexão com o banco de dados ao finalizar
    conn.close()

if __name__ == '__main__':
    run_pipeline()
