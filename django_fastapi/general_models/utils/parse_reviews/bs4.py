from datetime import datetime

import requests

from bs4 import BeautifulSoup

from .base import add_review_to_db


def get_exchange_list(exchange_name_set: set[str]):
    print(exchange_name_set)
    resp = requests.get('https://www.bestchange.ru/list.html')

    soup = BeautifulSoup(resp.text, 'lxml')

    rows = soup.find('table', id='content_table').find('tbody').find_all('tr')
    count = 1
    data_for_selenium = {}
    for row in rows:
        link = None
        name = row.find('td', class_='bj').text.lower()
        print(name)
        if name in exchange_name_set:
            link = row.find('td', class_='rw').find('a').get('href')
            print(count, name, link)
            count += 1
            # data = (name, link)
            # data_for_selenium.append(data)
            data_for_selenium[name] = link
    return data_for_selenium


def collect_data(review):
    header = review.find('div', class_='review_header')\
                    .find('table', class_='review_info')\
                    .find('tr').find_all('td')
    _, name, _, _, date  = header

    name = name.text
    date = date.find('span').get('title')
    valid_format_date = date[:20]
    date = datetime.strptime(valid_format_date, '%d.%m.%Y, %H:%M:%S')
    text = review.find('div', class_='review_middle')\
                    .find('div', class_='review_text').text
    return {
        'name': name,
        'text': text,
        'date': date,
    }


def parse_reviews(exchange_data: tuple[str, str],
                  marker: str,
                  limit: int = 20):
    exchange_name, link = exchange_data
    try:
        resp = requests.get(link, timeout=20)
    except Exception as ex:
        print(ex)
    else:
        html_text = resp.text
        soup = BeautifulSoup(html_text, 'lxml')
        reviews = soup.find('div', id='content_reviews')\
                        .find('div', class_='inner')\
                        .select("div[class*=review_block_]")
        print(len(reviews))

        for review in reviews[:limit]:
            try:
                review_data = collect_data(review)
            except Exception as ex:
                print(ex)
                continue
            else:
                add_review_to_db(exchange_name, review_data, marker)