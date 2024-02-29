import json

from django.core.management.base import BaseCommand, CommandError

from cash.models import Country, City


#Скрипт для создания городов в БД при запуске приложения
# python manage.py create_cities в docker-compose файле


parse_cities = {
    'Киев',
    'Чернигов',
    'Нью-Йорк',
    'Одесса',
    'Запорожье',
    'Варшава',
    'Ивано-Франковск',
    'Черкассы',
    'Краков',
    'Пхукет',
    'Ташкент',
    'Анталья',
    'Ереван',
    'Тбилиси',
    'Дубай',
    'Москва',
    'Алма-Ата',
    'Аланья',
    'Тирасполь',
    'Тель-Авив',
    'Санкт-Петербург',
    'Севастополь',
    'Краснодар',
    'Прага',
    'Астана',
    'Стамбул',
    'Сочи',
    'Ростов-На-Дону',
    'Казань',
    'Оренбург',
    'Уфа',
    'Екатеринбург',
    'Челябинск',
    'Воронеж',
    'Владивосток',
    'Калининград',
    'Нижний Новгород',
    'Иркутск',
    'Новосибирск',
}

class Command(BaseCommand):
    print('Creating Cities')

    def handle(self, *args, **kwargs):
        try:
                with open('ru_en_countries.json') as f:
                    json_data = json.load(f)

                for code_name, text in json_data.items():
                    ru, en = text.split('|')
                    ru_name, country_name = ru.split(', ')
                    en_name = en.split(',')[0]
                    country = Country.objects.get(name=country_name)

                    is_parse = False
                    if ru_name in parse_cities:
                        is_parse = True
                        
                    City.objects.create(name=ru_name,
                                        en_name=en_name,
                                        code_name=code_name,
                                        country=country,
                                        is_parse=is_parse)
        except Exception as ex:
            print(ex)
            raise CommandError('Initalization failed.')