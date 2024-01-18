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