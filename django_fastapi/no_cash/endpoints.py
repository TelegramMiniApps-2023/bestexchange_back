from fastapi import APIRouter, Request

from django.db.models import Count, Q
from django.db import connection

from general_models.utils.http_exc import http_exception_json
from general_models.utils.endpoints import (get_exchange_direction_list,
                                            get_valute_json,
                                            increase_popular_count_direction)

from .models import ExchangeDirection


no_cash_router = APIRouter(prefix='/no_cash',
                           tags=['Безналичные'])


# Вспомогательный эндпоинт для получения безналичных валют
def no_cash_valutes(request: Request,
                    params: dict):
    if not params['base']:
        http_exception_json(status_code=400, param='base')

    base = params['base']

    queries = ExchangeDirection.objects\
                                .select_related('exchange',
                                                'direction',
                                                'direction__valute_from',
                                                'direction__valute_to')\
                                .filter(is_active=True,
                                        exchange__is_active=True)

    if base == 'ALL':
        queries = queries.values_list('direction__valute_from').all()
    else:
        queries = queries.filter(direction__valute_from=base)\
                            .values_list('direction__valute_to').all()
        
    if not queries:
        http_exception_json(status_code=404, param=request.url)

    return get_valute_json(queries)


# Вспомогательный эндпоинт для получения безналичных готовых направлений
def no_cash_exchange_directions(request: Request,
                                params: dict):
    params.pop('city')
    for param in params:
        if not params[param]:
            http_exception_json(status_code=400, param=param)

    valute_from, valute_to = (params[key] for key in params)

    review_count_filter = Count('exchange__reviews',
                                filter=Q(exchange__reviews__moderation=True))
    queries = ExchangeDirection.objects\
                                .select_related('exchange',
                                                'direction',
                                                'direction__valute_from',
                                                'direction__valute_to')\
                                .annotate(review_count=review_count_filter)\
                                .filter(direction__valute_from=valute_from,
                                        direction__valute_to=valute_to,
                                        is_active=True,
                                        exchange__is_active=True)\
                                .order_by('-out_count', 'in_count').all()
    
    if not queries:
        http_exception_json(status_code=404, param=request.url)

    increase_popular_count_direction(valute_from=valute_from,
                                     valute_to=valute_to)
    
    return get_exchange_direction_list(queries,
                                       valute_from,
                                       valute_to)