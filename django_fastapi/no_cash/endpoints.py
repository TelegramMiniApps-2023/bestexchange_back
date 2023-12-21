from typing import List
from fastapi import APIRouter, Depends

from general_models.schemas import ValuteModel, SpecialDirectionModel
from general_models.utils.http_exc import http_exception_json
from general_models.utils.endpoints import (get_exchange_direction_list,
                                            get_valute_json)

from .utils.query_models import AvailbleValuteQuery, SpecificDirectionsQuery
from .models import ExchangeDirection


no_cash_router = APIRouter(prefix='/no_cash',
                           tags=['Безналичные'])


#Эндпоинт для получения доступных валют
@no_cash_router.get('/available_valutes',
                    response_model=dict[str, List[ValuteModel]] | list)
def get_available_valutes(base: AvailbleValuteQuery = Depends()):
    base = base.valute
    if not base:
        http_exception_json(status_code=400)

    if base == 'ALL':
        queries = ExchangeDirection.objects\
                                    .filter(is_active=True)\
                                    .values_list('valute_from').all()
    else:
        queries = ExchangeDirection.objects\
                                    .filter(is_active=True,
                                            valute_from=base)\
                                    .values_list('valute_to').all()
        
    if not queries:
        http_exception_json(status_code=404)

    return get_valute_json(queries)


#Эндпоинт для получения доступных готовых направлений
#по выбранным валютам
@no_cash_router.get('/directions',
                    response_model=List[SpecialDirectionModel] | None)
def get_specific_exchange_directions(query: SpecificDirectionsQuery = Depends()):
    if not all(param for param in query.params()):
        http_exception_json(status_code=400)
    
    valute_from, valute_to = query.params()

    queries = ExchangeDirection.objects\
                                .select_related('exchange')\
                                .filter(valute_from=valute_from,
                                        valute_to=valute_to,
                                        is_active=True,
                                        exchange__is_active=True).all()
    
    if not queries:
        http_exception_json(status_code=404)
    
    return get_exchange_direction_list(queries,
                                       valute_from,
                                       valute_to)