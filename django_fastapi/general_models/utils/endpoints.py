from typing import List
from collections import defaultdict

from django.conf import settings

from cash.models import ExchangeDirection as CashExDir
from no_cash.models import ExchangeDirection as NoCashExDir

from general_models.models import Valute
from general_models.schemas import ValuteModel


def try_generate_icon_url(valute: str | Valute) -> str | None:
    '''
    Генерирует путь иконки валюты.
    На вход принимает как объект Valute,
    так и кодовое сокращение валюты(BTC)
    '''
    
    if not isinstance(valute, Valute):
        valute = Valute.objects.get(code_name=valute)
    
    icon_url = None

    if valute.icon_url.name:
        icon_url = settings.PROTOCOL + settings.SITE_DOMAIN\
                                        + settings.DJANGO_PREFIX\
                                            + valute.icon_url.url
    return icon_url


def get_exchange_direction_list(queries: List[NoCashExDir | CashExDir],
                                valute_from: str,
                                valute_to: str,
                                city: str = None):
    icon_url_valute_from = try_generate_icon_url(valute_from)
    icon_url_valute_to = try_generate_icon_url(valute_to)

    direction_list = []

    partner_link_pattern = f'&cur_from={valute_from}&cur_to={valute_to}'
    if city:
        partner_link_pattern += f'&city={city}'

    for _id, query in enumerate(queries, start=1):
        if query.exchange.__dict__.get('partner_link'):
            query.exchange.__dict__['partner_link'] += partner_link_pattern
        exchange_direction = query.__dict__ | query.exchange.__dict__
        exchange_direction['id'] = _id
        exchange_direction['icon_valute_from'] = icon_url_valute_from
        exchange_direction['icon_valute_to'] = icon_url_valute_to
        direction_list.append(exchange_direction)

    return direction_list


def get_valute_json(queries: List[NoCashExDir | CashExDir]):
    valute_name_list = set(map(lambda query: query[0], queries))
    valutes = Valute.objects.filter(code_name__in=valute_name_list).all()
    
    default_dict_keys = {valute.type_valute for valute in valutes}
    
    json_dict = defaultdict(list)
    json_dict.fromkeys(default_dict_keys)

    for id, valute in enumerate(valutes, start=1):
        icon_url = try_generate_icon_url(valute)
        valute.icon_url = icon_url
        valute.id = id
        json_dict[valute.type_valute].append(ValuteModel(**valute.__dict__))

    return json_dict