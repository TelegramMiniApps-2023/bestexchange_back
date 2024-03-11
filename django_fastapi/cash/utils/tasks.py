from cash.models import Exchange

from django.db import connection


def get_cash_direction_set_for_creating(directions: set[tuple[str,str,str]],
                                        exchange: Exchange):
    '''
    Получить перечень направлений для создания
    '''

    exchange_directions = exchange\
                            .directions\
                            .select_related('city',
                                            'direction',
                                            'direction__valute_from',
                                            'direction__valute_to')\
                            .values_list('city__code_name',
                                         'direction__valute_from',
                                         'direction__valute_to').all()
    exchange_black_list_directions = exchange\
                                .direction_black_list\
                                .select_related('city',
                                                'direction',
                                                'direction__valute_from',
                                                'direction__valute_to')\
                                .values_list('city__code_name',
                                             'direction__valute_from',
                                             'direction__valute_to').all()
    checked_directions_by_exchange = exchange_black_list_directions.union(exchange_directions)

    directions -= set(checked_directions_by_exchange)
    print('DIRECTIONS FOR CREATING', directions)

    return directions


def generate_direction_dict(directions: set[str,str,str]):
    '''
    Генерирует словарь в формате: ключ - кодовое сокращение города,
    значение - список направлений. Пример направления: ('BTC', 'CASHRUB').
    '''
    direction_dict = {}
    for city, valute_from, valute_to in directions:
        direction_dict[city] = direction_dict.get(city, []) + [(valute_from, valute_to)]

    return direction_dict
