from typing import List

from django.db.models import Count, Q
from django.db import connection

from fastapi import APIRouter, Request

from general_models.utils.http_exc import http_exception_json
from general_models.utils.endpoints import (try_generate_icon_url,
                                            get_exchange_direction_list,
                                            get_valute_json)

from partners.utils.endpoints import get_partner_directions


from .models import Country, City, ExchangeDirection
from .schemas import MultipleName, RuEnCountryModel
from .utils.endpoints import get_available_countries


cash_router = APIRouter(prefix='/cash',
                        tags=['Наличные'])


# Эндпоинт для получения доступных стран
# и связанных с ними городов
@cash_router.get('/countries',
                 response_model=List[RuEnCountryModel],
                 response_model_by_alias=False)
def get_available_coutries(request: Request):
    cities = City.objects.filter(is_parse=True)\
                            .select_related('country').all()

    if not cities:
        http_exception_json(status_code=404, param=request.url)

    countries = get_available_countries(cities)

    # country_names = sorted({city.country.name for city in cities})
    
    # countries = Country.objects.filter(name__in=country_names)\
    #                             .prefetch_related('cities').all()

    # # print(len(connection.queries))
    # for country in countries:
    #     country.city_list = list(filter(lambda el: el.is_parse == True,
    #                                     country.cities.all()))

    #     for city in country.city_list:
    #         city.name = MultipleName(name=city.name,
    #                                  en_name=city.en_name)
        
    #     country.country_flag = try_generate_icon_url(country)

    #     country.name = MultipleName(name=country.name,
    #                                en_name=country.en_name)
    # print(len(connection.queries))
    return countries


# Вспомогательный эндпоинт для получения наличных валют
def cash_valutes(request: Request,
                 params: dict):
    for param in params:
        if not params[param]:
            http_exception_json(status_code=400, param=param)
    
    city, base = (params[key] for key in params)

    queries = ExchangeDirection.objects\
                                .select_related('exchange')\
                                .filter(city=city,
                                        is_active=True,
                                        exchange__is_active=True)

    if base == 'ALL':
        queries = queries.values_list('valute_from').all()
    else:
        queries = queries.filter(valute_from=base)\
                            .values_list('valute_to').all()
        
    if not queries:
        http_exception_json(status_code=404, param=request.url)

    return get_valute_json(queries)


# Вспомогательный эндпоинт для получения наличных готовых направлений
def cash_exchange_directions(request: Request,
                             params: dict):
    for param in params:
        if not params[param]:
            http_exception_json(status_code=400, param=param)

    city, valute_from, valute_to = (params[key] for key in params)

    review_count_filter = Count('exchange__reviews',
                                filter=Q(exchange__reviews__moderation=True))
    queries = ExchangeDirection.objects\
                                .select_related('exchange')\
                                .annotate(review_count=review_count_filter)\
                                .filter(city=city,
                                        valute_from=valute_from,
                                        valute_to=valute_to,
                                        is_active=True,
                                        exchange__is_active=True).all()

    
    partner_directions = get_partner_directions(city,
                                                valute_from,
                                                valute_to)
    
    queries = sorted(list(queries) + list(partner_directions),
                     key=lambda query: (-query.out_count, query.in_count))
    
    if not queries:
        http_exception_json(status_code=404, param=request.url)

    return get_exchange_direction_list(queries,
                                       valute_from,
                                       valute_to,
                                       city=city)