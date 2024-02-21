from typing import List
from fastapi import APIRouter, Depends, Request

from django.db.models import Count, Q

from general_models.schemas import ValuteModel, SpecialDirectionModel
from general_models.utils.http_exc import http_exception_json
from general_models.utils.endpoints import (get_exchange_direction_list,
                                            new_get_exchange_direction_list,
                                            get_valute_json,
                                            new_get_valute_json)

from .utils.query_models import AvailbleValuteQuery, SpecificDirectionsQuery
from .models import ExchangeDirection


no_cash_router = APIRouter(prefix='/no_cash',
                           tags=['Безналичные'])


#Эндпоинт для получения доступных валют
# @no_cash_router.get('/available_valutes',
#                     response_model=dict[str, List[ValuteModel]])
# def get_available_valutes(request: Request,
#                           query: AvailbleValuteQuery = Depends()):
#     for param in query.params():
#         if not query.params()[param]:
#             http_exception_json(status_code=400, param=param)

#     base = query.params()['base']

#     if base == 'ALL':
#         queries = ExchangeDirection.objects\
#                                     .select_related('exchange')\
#                                     .filter(is_active=True,
#                                             exchange__is_active=True)\
#                                     .values_list('valute_from').all()
#     else:
#         queries = ExchangeDirection.objects\
#                                     .select_related('exchange')\
#                                     .filter(is_active=True,
#                                             exchange__is_active=True,
#                                             valute_from=base)\
#                                     .values_list('valute_to').all()
        
#     if not queries:
#         http_exception_json(status_code=404, param=request.url)

#     return get_valute_json(queries)



##################
def no_cash_valutes(request: Request,
                    params: dict):
    if not params['base']:
        http_exception_json(status_code=400, param='base')

    base = params['base']

    queries = ExchangeDirection.objects\
                                .select_related('exchange')\
                                .filter(is_active=True,
                                        exchange__is_active=True)

    if base == 'ALL':
        queries = queries.values_list('valute_from').all()
    else:
        queries = queries.filter(valute_from=base)\
                            .values_list('valute_to').all()
        
    if not queries:
        http_exception_json(status_code=404, param=request.url)

    return get_valute_json(queries)


def new_no_cash_valutes(request: Request,
                        params: dict):
    if not params['base']:
        http_exception_json(status_code=400, param='base')

    base = params['base']

    queries = ExchangeDirection.objects\
                                .select_related('exchange')\
                                .filter(is_active=True,
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
#по выбранным валютам
# @no_cash_router.get('/directions',
#                     response_model=List[SpecialDirectionModel])
# def get_specific_exchange_directions(request: Request,
#                                      query: SpecificDirectionsQuery = Depends()):
#     for param in query.params():
#         if not query.params()[param]:
#             http_exception_json(status_code=400, param=param)
    
#     valute_from, valute_to = (query.params()[key] for key in query.params())

#     queries = ExchangeDirection.objects\
#                                 .select_related('exchange')\
#                                 .filter(valute_from=valute_from,
#                                         valute_to=valute_to,
#                                         is_active=True,
#                                         exchange__is_active=True).all()
    
#     if not queries:
#         http_exception_json(status_code=404, param=request.url)
    
#     return get_exchange_direction_list(queries,
#                                        valute_from,
#                                        valute_to)


##################
def no_cash_exchange_directions(request: Request,
                                params: dict):
    params.pop('city')
    for param in params:
        if not params[param]:
            http_exception_json(status_code=400, param=param)
    
    valute_from, valute_to = (params[key] for key in params)

    queries = ExchangeDirection.objects\
                                .select_related('exchange')\
                                .filter(valute_from=valute_from,
                                        valute_to=valute_to,
                                        is_active=True,
                                        exchange__is_active=True)\
                                .order_by('-out_count').all()
    
    if not queries:
        http_exception_json(status_code=404, param=request.url)
    
    return get_exchange_direction_list(queries,
                                       valute_from,
                                       valute_to)


###
def new_no_cash_exchange_directions(request: Request,
                                    params: dict):
    params.pop('city')
    for param in params:
        if not params[param]:
            http_exception_json(status_code=400, param=param)
    
    valute_from, valute_to = (params[key] for key in params)

    # queries = ExchangeDirection.objects\
    #                             .select_related('exchange')\
    #                             .filter(valute_from=valute_from,
    #                                     valute_to=valute_to,
    #                                     is_active=True,
    #                                     exchange__is_active=True)\
    #                             .order_by('-out_count', 'in_count').all()
    review_count_filter = Count('exchange__reviews',
                                filter=Q(exchange__reviews__moderation=True))
    queries = ExchangeDirection.objects\
                                .select_related('exchange')\
                                .annotate(review_count=review_count_filter)\
                                .filter(valute_from=valute_from,
                                        valute_to=valute_to,
                                        is_active=True,
                                        exchange__is_active=True)\
                                .order_by('-out_count', 'in_count').all()
    
    if not queries:
        http_exception_json(status_code=404, param=request.url)
    
    return new_get_exchange_direction_list(queries,
                                           valute_from,
                                           valute_to)