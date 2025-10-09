# app/parser.py
import httpx  # <-- Заменяем requests на httpx
from bs4 import BeautifulSoup

URL = 'https://lalafo.kg/kyrgyzstan/kvartiry/arenda-kvartir/2-bedrooms'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# v-- Добавляем async, чтобы функция стала асинхронной
async def parse_apartments():
    print("Начинаю асинхронный парсинг...")
    try:
        # v-- Используем асинхронный клиент httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(URL, headers=HEADERS, timeout=20)
            response.raise_for_status()
    except httpx.RequestError as e:
        print(f"Ошибка при запросе к сайту: {e}")
        return []

    # ... остальной код парсинга остается без изменений ...
    soup = BeautifulSoup(response.content, 'html.parser')
    apartments = []
    items = soup.find_all('article', class_='ad-tile-horizontal')
    for item in items:
        content_container = item.find('div', class_='ad-tile-horizontal-content-container')
        if not content_container:
            continue
        title_element = content_container.find('a', class_='ad-tile-horizontal-header-link-title')
        price_element = content_container.find('p', class_='LFSubHeading size-14 weight-700')
        if title_element and price_element:
            title = title_element.get_text(strip=True)
            price = price_element.get_text(strip=True)
            link = 'https://lalafo.kg' + title_element.get('href', '')
            apartments.append({'title': title, 'price': price, 'link': link})

    print(f"Парсинг завершен. Найдено {len(apartments)} объявлений.")
    return apartments