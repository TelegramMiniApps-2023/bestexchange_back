from typing import List

from django.db.models import Count, Q
from django.db import connection

from fastapi import APIRouter, Request

from general_models.utils.http_exc import http_exception_json
from general_models.utils.endpoints import (get_exchange_direction_list,
                                            get_valute_json,
                                            increase_popular_count_direction)

from partners.utils.endpoints import get_partner_directions
from partners.models import Direction as PartnerDirection

from .models import City, ExchangeDirection
from .schemas import RuEnCountryModel
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

    return countries


# Вспомогательный эндпоинт для получения наличных валют
def cash_valutes(request: Request,
                 params: dict):
    for param in params:
        if not params[param]:
            http_exception_json(status_code=400, param=param)
    
    city, base = (params[key] for key in params)

    cash_queries = ExchangeDirection.objects\
                                    .select_related('exchange',
                                                    'city',
                                                    'direction',
                                                    'direction__valute_from',
                                                    'direction__valute_to')\
                                    .filter(city__code_name=city,
                                            is_active=True,
                                            exchange__is_active=True)
    partner_queries = PartnerDirection.objects\
                                        .select_related('direction',
                                                        'city',
                                                        'direction__valute_from',
                                                        'direction__valute_to',
                                                        'city__exchange')\
                                        .filter(city__city__code_name=city,
                                                is_active=True,
                                                city__exchange__isnull=False)

    if base == 'ALL':
        cash_queries = cash_queries\
                                .values_list('direction__valute_from').all()
        partner_queries = partner_queries\
                                .values_list('direction__valute_from__code_name').all()
    else:
        cash_queries = cash_queries.filter(direction__valute_from=base)\
                                    .values_list('direction__valute_to').all()
        partner_queries = partner_queries.filter(direction__valute_from__code_name=base)\
                                        .values_list('direction__valute_to__code_name').all()

    queries = cash_queries.union(partner_queries)

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
                                .select_related('exchange',
                                                'city',
                                                'direction',
                                                'direction__valute_from',
                                                'direction__valute_to')\
                                .annotate(review_count=review_count_filter)\
                                .filter(city__code_name=city,
                                        direction__valute_from=valute_from,
                                        direction__valute_to=valute_to,
                                        is_active=True,
                                        exchange__is_active=True).all()

    
    partner_directions = get_partner_directions(city,
                                                valute_from,
                                                valute_to)
    
    queries = sorted(list(queries) + list(partner_directions),
                     key=lambda query: (-query.out_count, query.in_count))
    
    if not queries:
        http_exception_json(status_code=404, param=request.url)

    increase_popular_count_direction(valute_from=valute_from,
                                     valute_to=valute_to,
                                     city=city)

    return get_exchange_direction_list(queries,
                                       valute_from,
                                       valute_to,
                                       city=city)