from typing import List
from collections import defaultdict

from fastapi import APIRouter

from django.db.models import Q

from general_models.models import Valute
from general_models.utils.endpoints import try_generate_icon_url
from . import models, schemas


api_router = APIRouter()
no_cash_router = APIRouter(prefix='/no_cash',
                           tags=['No Cash', ])

#rating ?
@api_router.get("/directions", response_model=List[schemas.CurrentDirection])
def get_current_direction_list(valute_from: str, valute_to: str):
    valute_from, valute_to = valute_from.upper(), valute_to.upper()

    queries = models.ExchangeDirection.objects\
                    .filter(valute_from=valute_from,
                            valute_to=valute_to,
                            is_active=True)\
                    .select_related('exchange')\
                    .filter(exchange__is_active=True).all()
    
    #fix error in swagger
    if not queries:
        return []
    else:
        valute_from_obj = Valute.objects.get(code_name=valute_from)
        icon_url_valute_from = try_generate_icon_url(valute_from_obj)

        valute_to_obj = Valute.objects.get(code_name=valute_to)
        icon_url_valute_to = try_generate_icon_url(valute_to_obj)

        direction_list = []

        for count, query in enumerate(queries, start=1):
            if query.exchange.__dict__.get('partner_link'):
                query.exchange.__dict__['partner_link'] += f'&cur_from={valute_from}&cur_to={valute_to}'
            exchange_direction = query.__dict__ | query.exchange.__dict__
            exchange_direction['id'] = count
            exchange_direction['icon_valute_from'] = icon_url_valute_from
            exchange_direction['icon_valute_to'] = icon_url_valute_to
            direction_list.append(exchange_direction)

        return direction_list


@api_router.get('/available_directions')
def get_available_valute(base: str):
    base = base.upper()

    if base == 'ALL':
        queries = models.Direction.objects\
                    .select_related('valute_from')\
                    .order_by('valute_from__name')\
                    .distinct('valute_from__name').all()
        valute_list = [valute.valute_from for valute in queries]
    else:
        queries = models.Direction.objects\
                    .filter(valute_from=base)\
                    .select_related('valute_to').all()   
        valute_list = [valute.valute_to for valute in queries]

    if not queries:
        return []
    
    default_dict_keys = {valute.type_valute for valute in valute_list}
    
    json_dict = defaultdict(list)
    json_dict.fromkeys(default_dict_keys)

    for valute in valute_list:
        icon_url = try_generate_icon_url(valute)
        valute.icon_url = icon_url
        json_dict[valute.type_valute].append(schemas.NoCashValuteModel(**valute.__dict__))

    return json_dict


@api_router.get("/valute/no_cash")
def get_valute_list():
    valute_list = Valute.objects.filter(~Q(type_valute='Наличные')).all()

    type_valute_list = valute_list.values_list('type_valute')\
                                    .order_by('type_valute')\
                                    .distinct('type_valute')
    
    default_dict_keys = tuple(map(lambda el: el[0], type_valute_list))

    json_dict = defaultdict(list)
    json_dict.fromkeys(default_dict_keys)

    for valute in valute_list:
        icon_url = try_generate_icon_url(valute)
        valute.icon_url = icon_url
        json_dict[valute.type_valute].append(schemas.NoCashValuteModel(**valute.__dict__))

    return json_dict



##############
@no_cash_router.get('/directions', response_model=List[schemas.CurrentDirection] | None)
def get_current_exchange_directions(valute_from: str, valute_to: str = None):
    if valute_to is None:
        return None
    
    valute_from, valute_to = valute_from.upper(), valute_to.upper()

    queries = models.ExchangeDirection.objects\
                    .filter(valute_from=valute_from,
                            valute_to=valute_to,
                            is_active=True)\
                    .select_related('exchange')\
                    .filter(exchange__is_active=True).all()
    
    #fix error in swagger
    if not queries:
        return []
    else:
        valute_from_obj = Valute.objects.get(code_name=valute_from)
        icon_url_valute_from = try_generate_icon_url(valute_from_obj)

        valute_to_obj = Valute.objects.get(code_name=valute_to)
        icon_url_valute_to = try_generate_icon_url(valute_to_obj)

        direction_list = []

        for count, query in enumerate(queries, start=1):
            if query.exchange.__dict__.get('partner_link'):
                query.exchange.__dict__['partner_link'] += f'&cur_from={valute_from}&cur_to={valute_to}'
            exchange_direction = query.__dict__ | query.exchange.__dict__
            exchange_direction['id'] = count
            exchange_direction['icon_valute_from'] = icon_url_valute_from
            exchange_direction['icon_valute_to'] = icon_url_valute_to
            direction_list.append(exchange_direction)

        return direction_list
    

@no_cash_router.get('/available_valutes')
def get_available_valutes(base: str):
    base = base.upper()

    if base == 'ALL':
        queries = models.Direction.objects\
                    .select_related('valute_from')\
                    .order_by('valute_from__name')\
                    .distinct('valute_from__name').all()
        valute_list = [valute.valute_from for valute in queries]
    else:
        queries = models.Direction.objects\
                    .filter(valute_from=base)\
                    .select_related('valute_to').all()   
        valute_list = [valute.valute_to for valute in queries]

    if not queries:
        return []
    
    default_dict_keys = {valute.type_valute for valute in valute_list}
    
    json_dict = defaultdict(list)
    json_dict.fromkeys(default_dict_keys)

    for id, valute in enumerate(valute_list, start=1):
        icon_url = try_generate_icon_url(valute)
        valute.icon_url = icon_url
        valute.id = id
        json_dict[valute.type_valute].append(schemas.NewNoCashValute(**valute.__dict__))

    return json_dict