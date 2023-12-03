import json

import httpx
from bs4 import BeautifulSoup


async def fetch_api_data(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text


async def parse_and_sort(url: str):
    result_list = []
    data = await fetch_api_data(url)
    data = json.loads(data)

    for element in data:
        link = element.get('url', None)
        title = element.get('title', None)
        result_list.append({'link': link, 'title': title})
    return result_list


async def parse_last_article_on_page():
    page = await fetch_api_data('https://www.benzinga.com/markets')
    soup = BeautifulSoup(page, 'html.parser')
    article_body = soup.find('a', class_='newsfeed-card')
    href = article_body.get('href')
    article_number = href.split('/')[-2]
    return article_number


async def parse_article_content(url: str):
    page = await fetch_api_data(url)
    soup = BeautifulSoup(page, 'html.parser')

    article_body = soup.find('div', class_='article-content-body-only')

    article_content = ""

    for element in article_body.find_all(['p', 'ul', 'li'], class_='core-block'):
        if element.find('em', class_='core-block'):
            continue
        article_content += element.get_text(strip=True) + "\n"

    article_title = soup.find('h1', class_='layout-title').get_text()

    result_dict = {'title': article_title, 'content': article_content}

    return result_dict
