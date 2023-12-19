from typing import List
from fastapi import APIRouter, Depends

from general_models.schemas import ValuteModel, SpecialDirectionModel
from .utils.query_models import AvailbleValuteQuery, SpecificDirectionsQuery
from general_models.utils.endpoints import (get_exchange_direction_list,
                                            get_valute_json)

from .models import ExchangeDirection


no_cash_router = APIRouter(prefix='/no_cash',
                           tags=['Безналичные'])


@no_cash_router.get('/available_valutes',
                    response_model=dict[str, List[ValuteModel]] | list)
def get_available_valutes(base: AvailbleValuteQuery = Depends()):
    base = base.valute

    if base == 'ALL':
        queries = ExchangeDirection.objects\
                                    .filter(is_active=True)\
                                    .values_list('valute_from').all()
    else:
        queries = ExchangeDirection.objects\
                                    .filter(is_active=True,
                                            valute_from=base)\
                                    .values_list('valute_to').all()

    return get_valute_json(queries) if queries else []


@no_cash_router.get('/directions',
                    response_model=List[SpecialDirectionModel] | None)
def get_specific_exchange_directions(query: SpecificDirectionsQuery = Depends()):
    if not all(param for param in query.params()):
        return None
    
    valute_from, valute_to = query.params()

    queries = ExchangeDirection.objects\
                                .filter(valute_from=valute_from,
                                        valute_to=valute_to,
                                        is_active=True)\
                                .select_related('exchange')\
                                .filter(exchange__is_active=True).all()
    
    return [] if not queries else get_exchange_direction_list(queries,
                                                              valute_from,
                                                              valute_to)