import requests

from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError

from general_models.tasks import parse_reviews_with_start_service

from cash import models as cash_models
from no_cash import models as no_cash_models

# python manage.py parse_reviews_bs4
# При процессе запуска проекта использовать ТОЛЬКО одну из следующих команд:
# ЛИБО python manage.py parse_reviews_bs4, ЛИБО python manage.py parse_reviews_selenium !!!


class Command(BaseCommand):
    print('Parse reviews by exchanges with Beatiful Soap')

    def handle(self, *args, **kwargs):
        try:
            cash_exchange_list = cash_models.Exchange.objects.values('name').all()
            no_cash_exchange_list = no_cash_models.Exchange.objects.values('name').all()
            exchange_list = cash_exchange_list.union(no_cash_exchange_list)
            exchange_name_set = {exchange['name'].lower() for exchange in exchange_list}
            # print(exchange_name_set)
            # print(len(exchange_name_set))

            resp = requests.get('https://www.bestchange.ru/list.html')

            soup = BeautifulSoup(resp.text, 'lxml')

            rows = soup.find('table', id='content_table').find('tbody').find_all('tr')
            # count = 1
            data_for_selenium = {}
            for row in rows:
                link = None
                name = row.find('td', class_='bj').text.lower()
                if name in exchange_name_set:
                    link = row.find('td', class_='rw').find('a').get('href')
                    # print(count, name, link)
                    # count += 1
                    data_for_selenium[name] = link

            parse_reviews_with_start_service.delay(data_for_selenium)
            
        except Exception as ex:
            print(ex)
            raise CommandError('Initalization failed.')