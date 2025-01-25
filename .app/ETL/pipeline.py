import asyncio
import os

from telegram import Bot

from extract import pag_produto
from load import (configuracao_df, criando_conexao, get_max_price,
                  save_to_database)
from transform import parse_page

# Configuração do bot do Telegram
bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Função para enviar mensagem ao Telegram
async def send_telegram_message(text):
    """Envia uma mensagem para o Telegram."""
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text)
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Telegram: {e}")

# Função principal do pipeline
async def run_pipeline():
    """Executa o pipeline de extração, transformação e carga (ETL)."""
    conn = None
    try:
        conn = criando_conexao()  # Cria a conexão com o banco de dados
        configuracao_df(conn)  # Configura a tabela no banco de dados

        while True:
            # Etapa de extração: obtém o HTML da página do produto
            html = pag_produto()

            # Etapa de transformação: processa o HTML para extrair as informações desejadas
            data = parse_page(html)
            current_price = data['preco_atual']

            # Etapa de carga: verifica o maior preço e envia mensagem se necessário
            max_price, max_price_timestamp = get_max_price(conn)

            if max_price is None or current_price > max_price:
                # Novo maior preço detectado
                await send_telegram_message(f"Novo preço maior detectado: {current_price}")
            else:
                # O maior preço registrado já é o atual
                await send_telegram_message(f"O maior preço registrado é {max_price} em {max_price_timestamp}")

            # Salva os dados no banco de dados
            save_to_database(data)

            # Aguarda 10 segundos antes de realizar a próxima execução
            await asyncio.sleep(10)
    
    except KeyboardInterrupt:
        print("Execução interrompida.")
    except Exception as e:
        print(f"Ocorreu um erro durante a execução do pipeline: {e}")
    finally:
        if conn:
            conn.close()  # Garante que a conexão seja fechada no final

# Inicia a execução do pipeline de forma assíncrona
if __name__ == "__main__":
    asyncio.run(run_pipeline())



# import asyncio
# from extract import pag_produto
# from transform import parse_page
# from load import criando_conexao, configuracao_df, save_to_database, get_max_price
# from telegram import Bot
# import os

# bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
# CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# async def send_telegram_message(text):
#     """Envia uma mensagem para o Telegram."""
#     await bot.send_message(chat_id=CHAT_ID, text=text)

# async def run_pipeline():
#     conn = criando_conexao()
#     configuracao_df(conn)
#     try:
#         while True:
#             html = pag_produto()
#             data = parse_page(html)
#             current_price = data['preco_atual']

#             max_price, max_price_timestamp = get_max_price(conn)
#             if max_price is None or current_price > max_price:
#                 await send_telegram_message(f"Novo preço maior detectado: {current_price}")
#             else:
#                 await send_telegram_message(f"O maior preço registrado é {max_price} em {max_price_timestamp}")

#             save_to_database(data)
#             await asyncio.sleep(10)
#     except KeyboardInterrupt:
#         print("Execução interrompida.")
#     finally:
#         conn.close()
