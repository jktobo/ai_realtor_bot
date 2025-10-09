# app/ai_processor.py
import os
from openai import OpenAI
import json

# Инициализируем клиент OpenAI, он автоматически подхватит ключ из .env
client = OpenAI()

def get_search_parameters(query: str):
    print(f"Отправляю в AI запрос: {query}")

    system_prompt = """
    Ты — умный ассистент по подбору недвижимости в Бишкеке. 
    Твоя задача — извлечь из текста пользователя параметры для поиска и вернуть их в формате JSON.

    Возможные параметры:
    - "rooms": количество комнат (число: 1, 2, 3 и т.д.).
    - "price_max": максимальная цена (число).
    - "currency": валюта ("KGS" или "USD").
    - "city": город ("Бишкек" - это значение по умолчанию).

    Если какой-то параметр не указан, не включай его в JSON.
    Если не можешь определить параметры, верни пустой JSON {}.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
        )
        json_response_str = response.choices[0].message.content
        print(f"AI вернул параметры: {json_response_str}")
        # Преобразуем строку JSON в словарь Python
        return json.loads(json_response_str)
    except Exception as e:
        print(f"Ошибка при обращении к OpenAI: {e}")
        return {} # Возвращаем пустой словарь в случае ошибки