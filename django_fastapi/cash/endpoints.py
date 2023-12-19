from typing import List

from fastapi import APIRouter, Depends

from general_models.utils.endpoints import (get_exchange_direction_list,
                                            get_valute_json)

from general_models.schemas import ValuteModel
from .utils.query_models import (AvailableCitiesQuery,
                                 AvailableValutesQuery,
                                 SpecificDirectionsQuery)

from .models import Country, City, ExchangeDirection
from .schemas import CountryModel, CityModel, SpecialCashDirectionModel


cash_router = APIRouter(prefix='/cash',
                        tags=['Наличные'])


@cash_router.get('/countries',
                 response_model=List[CountryModel],
                 response_model_by_alias=False)
def get_available_coutries():
    countries = City.objects.filter(is_parse=True)\
                            .select_related('country')\
                            .values('country__pk', 'country__name')\
                            .order_by('country__name')\
                            .distinct('country__name').all()
    return countries


@cash_router.get('/available_cities',
                 response_model=List[CityModel],
                 response_model_by_alias=False)
def get_available_cities_for_current_country(query: AvailableCitiesQuery = Depends()):
    country = query.country
    cities = Country.objects.get(name=country)\
                    .cities.filter(is_parse=True).all()
    return cities


@cash_router.get('/available_valutes',
                 response_model=dict[str, List[ValuteModel]] | list)
def get_available_valutes_for_current_city(query: AvailableValutesQuery = Depends()):
    city, base = query.params()
    
    queries = ExchangeDirection.objects\
                                .filter(is_active=True,
                                        city=city)

    if base == 'ALL':
        queries = queries.values_list('valute_from').all()
    else:
        queries = queries.filter(valute_from=base)\
                            .values_list('valute_to').all()

    return get_valute_json(queries) if queries else []


@cash_router.get('/directions',
                 response_model=List[SpecialCashDirectionModel] | None)
def get_current_exchange_directions(query: SpecificDirectionsQuery = Depends()):
    if not all(param for param in query.params()):
        return None

    city, valute_from, valute_to = query.params()

    queries = ExchangeDirection.objects\
                                .filter(city=city,
                                        valute_from=valute_from,
                                        valute_to=valute_to).all()

    return [] if not queries else get_exchange_direction_list(queries,
                                                              valute_from,
                                                              valute_to,
                                                              city=city)