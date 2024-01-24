from bs4 import BeautifulSoup

from cash import models as cash_models
from no_cash import models as no_cash_models


def get_exchange_list(marker: str = None):
    match marker:
        case 'no_cash':
            exchange_list = cash_models.Exchange.objects.values('name').all()
        case 'cash':
            exchange_list = no_cash_models.Exchange.objects.values('name').all()
        case _:
            cash_exchange_list = cash_models.Exchange.objects.values('name').all()
            no_cash_exchange_list = no_cash_models.Exchange.objects.values('name').all()
            exchange_list = cash_exchange_list.union(no_cash_exchange_list)

    return exchange_list


def make_valid_values_for_dict(dict_for_exchange_direction: dict):
    in_count = float(dict_for_exchange_direction['in_count'])
    out_count = float(dict_for_exchange_direction['out_count'])

    if out_count < 1:
        k = 1 / out_count
        out_count = 1
        in_count *= k
        dict_for_exchange_direction['in_count'] = in_count
        dict_for_exchange_direction['out_count'] = out_count