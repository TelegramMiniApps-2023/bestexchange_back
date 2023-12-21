from typing import List

from fastapi import APIRouter, Depends

from general_models.schemas import ValuteModel
from general_models.utils.http_exc import http_exception_json
from general_models.utils.endpoints import (get_exchange_direction_list,
                                            get_valute_json)

from .utils.query_models import (AvailableCitiesQuery,
                                 AvailableValutesQuery,
                                 SpecificDirectionsQuery)
from .models import Country, City, ExchangeDirection
from .schemas import CountryModel, CityModel, SpecialCashDirectionModel


cash_router = APIRouter(prefix='/cash',
                        tags=['Наличные'])


#Эндпоинт для получения доступных стран
@cash_router.get('/countries',
                 response_model=List[CountryModel],
                 response_model_by_alias=False)
def get_available_coutries():
    countries = City.objects.filter(is_parse=True)\
                            .select_related('country')\
                            .values('country__pk', 'country__name')\
                            .order_by('country__name')\
                            .distinct('country__name').all()
    
    if not countries:
        http_exception_json(status_code=404)
    
    return countries


#Эндпоинт для получения доступных городов выбранной страны
@cash_router.get('/available_cities',
                 response_model=List[CityModel],
                 response_model_by_alias=False)
def get_available_cities_for_current_country(query: AvailableCitiesQuery = Depends()):
    country = query.country
    if not country:
        http_exception_json(status_code=400)

    #из-за метода get
    try:
        cities = Country.objects.get(name=country)\
                        .cities.filter(is_parse=True).all()
    except Exception:
        http_exception_json(status_code=404)
    else:
        if not cities:
            http_exception_json(status_code=404)
        
        return cities


#Эндпоинт для получения доступных валют выбранного города
@cash_router.get('/available_valutes',
                 response_model=dict[str, List[ValuteModel]])
def get_available_valutes_for_current_city(query: AvailableValutesQuery = Depends()):
    if not all(param for param in query.params()):
        http_exception_json(status_code=400)
    
    city, base = query.params()
    queries = ExchangeDirection.objects\
                                .filter(city=city,
                                        is_active=True)

    if base == 'ALL':
        queries = queries.values_list('valute_from').all()
    else:
        queries = queries.filter(valute_from=base)\
                            .values_list('valute_to').all()
        
    if not queries:
        http_exception_json(status_code=404)

    return get_valute_json(queries)


#Эндпоинт для получения доступных готовых направлений
#по выбранным валютам и городу
@cash_router.get('/directions',
                 response_model=List[SpecialCashDirectionModel])
def get_current_exchange_directions(query: SpecificDirectionsQuery = Depends()):
    if not all(param for param in query.params()):
        http_exception_json(status_code=400)

    city, valute_from, valute_to = query.params()

    queries = ExchangeDirection.objects\
                                .select_related('exchange')\
                                .filter(city=city,
                                        valute_from=valute_from,
                                        valute_to=valute_to,
                                        is_active=True,
                                        exchange__is_active=True).all()
    
    if not queries:
        http_exception_json(status_code=404)

    return get_exchange_direction_list(queries,
                                       valute_from,
                                       valute_to,
                                       city=city)