# app/main.py

from fastapi import FastAPI, Request
import telegram
import os
from dotenv import load_dotenv

# --- НОВОЕ: Импортируем нашу функцию парсера ---
from .parser import parse_apartments

# Загружаем переменные из .env файла
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
app = FastAPI()

@app.post("/webhook")
async def webhook(req: Request):
    body = await req.json()
    update = telegram.Update.de_json(body, bot)

    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text

        # --- НОВОЕ: Логика обработки команд ---
        if text == '/start':
            await bot.send_message(chat_id=chat_id, text="Привет! Отправь мне /search, чтобы найти квартиры.")
        
        elif text == '/search':
            await bot.send_message(chat_id=chat_id, text="Ищу объявления по умолчанию (2-комнатные)...")

            # v-- ГЛАВНОЕ ИЗМЕНЕНИЕ: добавляем await
            apartments = await parse_apartments()

            if apartments:
                # Отправляем только первые 5, чтобы не спамить в чат
                for apt in apartments[:5]:
                    # Форматируем сообщение с использованием Markdown для красивых ссылок
                    message = (
                        f"**{apt['title']}**\n"
                        f"Цена: {apt['price']}\n\n"
                        f"[Посмотреть на lalafo]({apt['link']})"
                    )
                    await bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                await bot.send_message(chat_id=chat_id, text="К сожалению, по вашему запросу ничего не найдено.")

        else:
            await bot.send_message(chat_id=chat_id, text=f"Неизвестная команда. Попробуйте /start или /search.")

    return {"status": "ok"}


@app.get("/")
def read_root():
    return {"Hello": "World"}