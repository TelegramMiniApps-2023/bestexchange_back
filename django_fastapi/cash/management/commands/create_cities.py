from django.core.management.base import BaseCommand, CommandError

from cash.models import Country, City


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
            for city in open('cities.txt'):
                city = tuple(map(lambda el: el.strip(), city.split(',')))
                code_name, name, country_name = city
                country = Country.objects.get(name=country_name)

                is_parse = False
                if name in parse_cities:
                    is_parse = True
                    
                City.objects.create(name=name,
                                    code_name=code_name,
                                    country=country,
                                    is_parse=is_parse)
        except Exception as ex:
            print(ex)
            raise CommandError('Initalization failed.')