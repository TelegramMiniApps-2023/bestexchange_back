from django.core.management.base import BaseCommand, CommandError

import requests

from bs4 import BeautifulSoup, NavigableString

from no_cash.models import Exchange, Rating


class Command(BaseCommand):
    print('Creating Rating')

    def handle(self, *args, **kwargs):
        try:
            def parse_rate():
                resp = requests.get('https://www.bestchange.ru/list.html')

                soup = BeautifulSoup(resp.text, 'lxml')
                rows = soup.find('table', id='content_table').find('tbody').find_all('td', class_='rw')
                
                if rows: 
                    rating_dict = {}

                    for row in rows:
                        row: NavigableString
                        exchange_name = row.find('a').get('title').split()[-1]
                        rating_table = row.find('table').find('tr').find_all('td')
                        rating = []
                        for rating_part in rating_table:
                            if rating_part.text.isdigit():
                                rating.append(rating_part.text)
                        rating_dict[exchange_name] = '/'.join(rating[::-1])

                    return rating_dict
                

            def create_rating():
                check = Rating.objects.first()
                if not check:
                    exchange_list = Exchange.objects.all()
                    print('check 1')
                    rating_dict = parse_rate()
                    for exchange in exchange_list:
                        Rating.objects.create(exchange_name=exchange.name,
                                            rating=rating_dict.get(exchange.name),
                                            exchange=exchange)
                        print('check 2')


            create_rating()
        except Exception as ex:
            print(ex)
            raise CommandError('Initalization failed.')