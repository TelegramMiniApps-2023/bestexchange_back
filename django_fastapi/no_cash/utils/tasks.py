from django.core.cache import cache

from no_cash.models import Direction, Exchange


def get_or_set_no_cash_directions_cache():
    '''
    Получить или установить кэш значение безналичных направлений
    '''

    if not (all_no_cash_directions := cache.get('all_no_cash_directions', False)):
        print('SET VALUE TO CACHE')
        all_no_cash_directions = Direction.objects\
                                .select_related('valute_from', 'valute_to')\
                                .values_list('valute_from', 'valute_to').all()
        cache.set('all_no_cash_directions', all_no_cash_directions, 60)#вывести время в settings
    return set(all_no_cash_directions)


def get_no_cash_direction_set_for_creating(directions: set[tuple[str,str]],
                                           exchange: Exchange):
    '''
    Получить перечень направлений для создания
    '''

    exchange_directions = exchange.directions\
                                .values_list('valute_from', 'valute_to').all()
    exchange_black_list_directions = exchange.direction_black_list\
                                .values_list('valute_from', 'valute_to').all()
    checked_directions_by_exchange = exchange_black_list_directions.union(exchange_directions)
    # print('ALL DIRECTION', directions)
    # print('EXCHANGE DIRECTION', exchange_directions)
    # print('BLACK LIST', exchange_black_list_directions)
    # directions -= set(exchange_directions)
    # directions -= set(exchange_black_list_directions)
    directions -= set(checked_directions_by_exchange)
    print('DIRECTION FOR CREATING', directions)
    return directions