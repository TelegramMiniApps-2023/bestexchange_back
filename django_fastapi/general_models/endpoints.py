from typing import List

from fastapi import APIRouter, Request, Depends

from no_cash.endpoints import no_cash_valutes, no_cash_exchange_directions

from cash.endpoints import cash_valutes, cash_exchange_directions
from cash.schemas import SpecialCashDirectionModel

from .utils.query_models import AvailableValutesQuery, SpecificDirectionsQuery
from .utils.http_exc import http_exception_json
from .schemas import ValuteModel, SpecialDirectionModel


common_router = APIRouter(tags=['Общее'])


#Эндпоинт для получения доступных валют выбранного города
@common_router.get('/available_valutes',
                 response_model=dict[str, List[ValuteModel]])
def get_available_valutes(request: Request,
                          query: AvailableValutesQuery = Depends()):
    params = query.params()
    if not params['city']:
        json_dict = no_cash_valutes(request, params)
    else:
        json_dict = cash_valutes(request, params)
    
    return json_dict


#Эндпоинт для получения доступных готовых направлений
#по выбранным валютам и городу
@common_router.get('/directions',
                 response_model=List[SpecialCashDirectionModel | SpecialDirectionModel])
def get_current_exchange_directions(request: Request,
                                    query: SpecificDirectionsQuery = Depends()):
    params = query.params()
    if not params['city']:
        json_dict = no_cash_exchange_directions(request, params)
    else:
        json_dict = cash_exchange_directions(request, params)
    
    return json_dict