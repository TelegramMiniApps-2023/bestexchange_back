from typing import List
from collections import defaultdict

from fastapi import APIRouter, Depends, Request

from django.conf import settings

from general_models.schemas import ValuteModel
from general_models.utils.http_exc import http_exception_json
from general_models.utils.endpoints import (try_generate_icon_url,
                                            get_exchange_direction_list,
                                            new_get_exchange_direction_list,
                                            get_valute_json,
                                            new_get_valute_json)

from .utils.query_models import (AvailableCitiesQuery,
                                 AvailableValutesQuery,
                                 SpecificDirectionsQuery)
from .models import Country, City, ExchangeDirection
from .schemas import (CountryModel,
                      CityModel,
                      SpecialCashDirectionModel,
                      MultipleName,
                      RuEnCityModel,
                      RuEnCountryModel)


cash_router = APIRouter(prefix='/cash',
                        tags=['Наличные'])


#Эндпоинт для получения доступных стран
# @cash_router.get('/countries',
#                  response_model=List[CountryModel],
#                  response_model_by_alias=False)
# def get_available_coutries():
#     countries = City.objects.filter(is_parse=True)\
#                             .select_related('country')\
#                             .values('country__pk', 'country__name')\
#                             .order_by('country__name')\
#                             .distinct('country__name').all()
    
#     if not countries:
#         http_exception_json(status_code=404)
    
#     return countries


#Эндпоинт для получения доступных стран
#и связанных городов
@cash_router.get('/countries',
                 response_model=List[CountryModel],
                 response_model_by_alias=False)
def get_available_coutries(request: Request):
    cities = City.objects.filter(is_parse=True)\
                            .select_related('country').all()
    
    if not cities:
        http_exception_json(status_code=404, param=request.url)

    countries = sorted({city.country for city in cities},
                       key=lambda country: country.name)

    for country in countries:
        country.city_list = country.cities\
                                    .filter(is_parse=True)\
                                    .order_by('name').all()
        country.country_flag = try_generate_icon_url(country)

    return countries


#Эндпоинт для получения доступных стран
#и связанных городов (мультиязычность)
@cash_router.get('/countries_multi',
                 response_model=List[RuEnCountryModel],
                 response_model_by_alias=False)
def get_available_coutries(request: Request):
    cities = City.objects.filter(is_parse=True)\
                            .select_related('country').all()
    
    if not cities:
        http_exception_json(status_code=404, param=request.url)

    countries = sorted({city.country for city in cities},
                       key=lambda country: country.name)

    for country in countries:
        country.city_list = country.cities\
                                    .filter(is_parse=True)\
                                    .order_by('name').all()
        for city in country.city_list:
            city.name = MultipleName(name=city.name,
                                     en_name=city.en_name)
        
        country.country_flag = try_generate_icon_url(country)

        country.name = MultipleName(name=country.name,
                                   en_name=country.en_name)

    return countries


#Эндпоинт для получения доступных городов выбранной страны
@cash_router.get('/available_cities',
                 response_model=List[CityModel],
                 response_model_by_alias=False)
def get_available_cities_for_current_country(request: Request,
                                             query: AvailableCitiesQuery = Depends()):
    for param in query.params():
        if not query.params()[param]:
            http_exception_json(status_code=400, param=param)

    country = query.params()['country']

    #из-за метода get
    try:
        cities = Country.objects.get(name=country)\
                        .cities.filter(is_parse=True).all()
    except Exception:
        http_exception_json(status_code=404, param=request.url)
    else:
        if not cities:
            http_exception_json(status_code=404, param=request.url)
        
        return cities


#Эндпоинт для получения доступных валют выбранного города
@cash_router.get('/available_valutes',
                 response_model=dict[str, List[ValuteModel]])
def get_available_valutes_for_current_city(request: Request,
                                           query: AvailableValutesQuery = Depends()):
    for param in query.params():
        if not query.params()[param]:
            http_exception_json(status_code=400, param=param)
    
    city, base = (query.params()[key] for key in query.params())

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


##################
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


def new_cash_valutes(request: Request,
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

    return new_get_valute_json(queries)


#Эндпоинт для получения доступных готовых направлений
#по выбранным валютам и городу
@cash_router.get('/directions',
                 response_model=List[SpecialCashDirectionModel])
def get_current_exchange_directions(request: Request,
                                    query: SpecificDirectionsQuery = Depends()):
    for param in query.params():
        if not query.params()[param]:
            http_exception_json(status_code=400, param=param)

    city, valute_from, valute_to = (query.params()[key] for key in query.params())

    queries = ExchangeDirection.objects\
                                .select_related('exchange')\
                                .filter(city=city,
                                        valute_from=valute_from,
                                        valute_to=valute_to,
                                        is_active=True,
                                        exchange__is_active=True)\
                                .order_by('-out_count').all()
    
    if not queries:
        http_exception_json(status_code=404, param=request.url)

    return get_exchange_direction_list(queries,
                                       valute_from,
                                       valute_to,
                                       city=city)



#############################
def cash_exchange_directions(request: Request,
                             params: dict):
    for param in params:
        if not params[param]:
            http_exception_json(status_code=400, param=param)

    city, valute_from, valute_to = (params[key] for key in params)

    queries = ExchangeDirection.objects\
                                .select_related('exchange')\
                                .filter(city=city,
                                        valute_from=valute_from,
                                        valute_to=valute_to,
                                        is_active=True,
                                        exchange__is_active=True)\
                                .order_by('-out_count').all()
    
    if not queries:
        http_exception_json(status_code=404, param=request.url)

    return get_exchange_direction_list(queries,
                                       valute_from,
                                       valute_to,
                                       city=city)



def new_cash_exchange_directions(request: Request,
                                 params: dict):
    for param in params:
        if not params[param]:
            http_exception_json(status_code=400, param=param)

    city, valute_from, valute_to = (params[key] for key in params)

    queries = ExchangeDirection.objects\
                                .select_related('exchange')\
                                .filter(city=city,
                                        valute_from=valute_from,
                                        valute_to=valute_to,
                                        is_active=True,
                                        exchange__is_active=True)\
                                .order_by('-out_count').all()
    
    if not queries:
        http_exception_json(status_code=404, param=request.url)

    return new_get_exchange_direction_list(queries,
                                           valute_from,
                                           valute_to,
                                           city=city)