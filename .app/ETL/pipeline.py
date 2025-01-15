import asyncio
from extract import pag_produto
from transform import parse_page
from load import criando_conexao, configuracao_df, save_to_database, get_max_price
from telegram import Bot
import os

bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

async def send_telegram_message(text):
    """Envia uma mensagem para o Telegram."""
    await bot.send_message(chat_id=CHAT_ID, text=text)

async def run_pipeline():
    conn = criando_conexao()
    configuracao_df(conn)
    try:
        while True:
            html = pag_produto()
            data = parse_page(html)
            current_price = data['preco_atual']

            max_price, max_price_timestamp = get_max_price(conn)
            if max_price is None or current_price > max_price:
                await send_telegram_message(f"Novo preço maior detectado: {current_price}")
            else:
                await send_telegram_message(f"O maior preço registrado é {max_price} em {max_price_timestamp}")

            save_to_database(data)
            await asyncio.sleep(10)
    except KeyboardInterrupt:
        print("Execução interrompida.")
    finally:
        conn.close()
