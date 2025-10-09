# app/parser.py
import httpx
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla.5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Теперь функция принимает URL как аргумент
async def parse_apartments(target_url: str):
    print(f"Начинаю асинхронный парсинг по URL: {target_url}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(target_url, headers=HEADERS, timeout=20, follow_redirects=True)
            response.raise_for_status() 
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        print(f"Ошибка при запросе к сайту: {e}")
        return []

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