from typing import List

from fastapi import APIRouter, Request, Depends

from no_cash.endpoints import (no_cash_valutes,
                               no_cash_exchange_directions,
                               new_no_cash_exchange_directions,
                               new_no_cash_valutes)

from cash.endpoints import cash_valutes, cash_exchange_directions, new_cash_valutes, new_cash_exchange_directions
from cash.schemas import SpecialCashDirectionModel, SpecialCashDirectionMultiModel
#
from cash.models import Direction
#

from .utils.query_models import AvailableValutesQuery, SpecificDirectionsQuery
from .utils.http_exc import http_exception_json
from .schemas import ValuteModel, SpecialDirectionModel, EnValuteModel, SpecialDirectionMultiModel


common_router = APIRouter(tags=['Общее'])


#Эндпоинт для получения доступных валют выбранного города
# @common_router.get('/available_valutes',
#                  response_model=dict[str, List[ValuteModel]])
# def get_available_valutes(request: Request,
#                           query: AvailableValutesQuery = Depends()):
#     params = query.params()
#     if not params['city']:
#         json_dict = no_cash_valutes(request, params)
#     else:
#         json_dict = cash_valutes(request, params)
    
#     return json_dict

@common_router.get('/available_valutes',
                 response_model=dict[str, dict[str, List[ValuteModel | EnValuteModel]]])
def get_available_valutes(request: Request,
                          query: AvailableValutesQuery = Depends()):
    params = query.params()
    if not params['city']:
        json_dict = new_no_cash_valutes(request, params)
    else:
        json_dict = new_cash_valutes(request, params)
    
    return json_dict


@common_router.get('/available_valutes_multi',
                 response_model=dict[str, dict[str, List[ValuteModel | EnValuteModel]]])
def get_available_valutes(request: Request,
                          query: AvailableValutesQuery = Depends()):
    params = query.params()
    if not params['city']:
        json_dict = new_no_cash_valutes(request, params)
    else:
        json_dict = new_cash_valutes(request, params)
    
    return json_dict


#Эндпоинт для получения доступных готовых направлений
#по выбранным валютам и городу
# @common_router.get('/directions',
#                  response_model=List[SpecialCashDirectionModel | SpecialDirectionModel])
# def get_current_exchange_directions(request: Request,
#                                     query: SpecificDirectionsQuery = Depends()):
#     params = query.params()
#     if not params['city']:
#         json_dict = no_cash_exchange_directions(request, params)
#     else:
#         json_dict = cash_exchange_directions(request, params)
    
#     return json_dict

@common_router.get('/directions',
                 response_model=List[SpecialCashDirectionMultiModel | SpecialDirectionMultiModel],
                 response_model_by_alias=False)
def get_current_exchange_directions(request: Request,
                                    query: SpecificDirectionsQuery = Depends()):
    params = query.params()
    if not params['city']:
        json_dict = new_no_cash_exchange_directions(request, params)
    else:
        json_dict = new_cash_exchange_directions(request, params)
    
    return json_dict


@common_router.get('/directions_multi',
                 response_model=List[SpecialCashDirectionMultiModel | SpecialDirectionMultiModel],
                 response_model_by_alias=False)
def get_current_exchange_directions(request: Request,
                                    query: SpecificDirectionsQuery = Depends()):
    params = query.params()
    if not params['city']:
        json_dict = new_no_cash_exchange_directions(request, params)
    else:
        json_dict = new_cash_exchange_directions(request, params)
    
    return json_dict

###
@common_router.get('/actual_course')
def get_actual_course_for_direction(valute_from: str, valute_to: str):
    direction = Direction.objects.get(display_name=f'{valute_from.upper()} -> {valute_to.upper()}')
    # print(direction.actual_course)
    return direction.actual_course