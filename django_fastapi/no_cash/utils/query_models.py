from fastapi import Query
from fastapi.openapi.models import Example


#Описание для Swagger`a
#Query параметры для эндпоинта /available_valutes
class AvailbleValuteQuery:
    def __init__(self,
                 base: str = Query(description='Кодовое сокращение валюты',
                                   openapi_examples={
                                        'Валюты, доступные для обмена': Example(value='all'),
                                        'Валюты, в которые можно обменять': Example(value='btc'),
                                   })):
        self.valute = base.upper()


#Описание для Swagger`a
#Query параметры для эндпоинта /directions
class SpecificDirectionsQuery:
    def __init__(self,
                 valute_from: str = Query(description='Кодовое сокращение валюты',
                                          example='btc'),
                 valute_to: str = Query(description='Кодовое сокращение валюты',
                                        example='sberrub')):
        self.valute_from = valute_from.upper()
        self.valute_to = valute_to.upper()

    def params(self):
        return (self.valute_from, self.valute_to)