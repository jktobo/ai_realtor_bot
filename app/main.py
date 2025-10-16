# app/main.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
import telegram
import os
from telegram.constants import ParseMode

# --- ИЗМЕНЕНИЕ: Убираем точки, делаем импорты абсолютными ---
from parser import parse_apartments
from ai_processor import get_search_parameters

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
app = FastAPI()

# ... остальной код остается без изменений ...

@app.post("/webhook")
async def webhook(req: Request):
    body = await req.json()
    update = telegram.Update.de_json(body, bot)

    if not update.message:
        return {"status": "ok"}

    chat_id = update.message.chat.id
    text = update.message.text

    if text == '/start':
        await bot.send_message(
            chat_id=chat_id, 
            text="Привет! Напиши, какую квартиру ты ищешь. Например: 'ищу 2-комнатную в центре до 500$'"
        )
    else: 
        await bot.send_message(chat_id=chat_id, text="Анализирую ваш запрос с помощью AI...")
        
        params = get_search_parameters(text)

        if not params:
            await bot.send_message(chat_id=chat_id, text="Не смог распознать параметры. Попробуйте переформулировать.")
            return {"status": "ok"}

        rooms = params.get("rooms", "")
        base_url = f"https://lalafo.kg/kyrgyzstan/kvartiry/arenda-kvartir/{rooms}-bedrooms" if rooms else "https://lalafo.kg/kyrgyzstan/kvartiry/arenda-kvartir"
        
        await bot.send_message(chat_id=chat_id, text=f"Понял. Ищу по запросу: {text}\nНачинаю парсинг...")
        
        apartments = await parse_apartments(base_url)

        if not apartments:
            await bot.send_message(chat_id=chat_id, text="К сожалению, ничего не найдено. Попробуйте другой запрос.")
            return {"status": "ok"}
        
        await bot.send_message(chat_id=chat_id, text=f"Найдено {len(apartments)} объявлений. Вот первые 5:")
        for apt in apartments[:5]:
            message = (
                f"*{apt['title']}*\n"
                f"Цена: {apt['price']}\n\n"
                f"[Посмотреть на lalafo]({apt['link']})"
            )
            await bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN_V2)

    return {"status": "ok"}