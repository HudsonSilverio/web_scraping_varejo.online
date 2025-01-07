
import asyncio
from telegram import Bot

TELEGRAM_TOKEN = "8068436836:AAGfDzr3J0ah6BQxrucG-Qt06uV9ANHXn1E"
TELEGRAM_CHAT_ID = "6816017490"

async def send_message():
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Teste de mensagem!")

# Executa a função assíncrona
asyncio.run(send_message())
