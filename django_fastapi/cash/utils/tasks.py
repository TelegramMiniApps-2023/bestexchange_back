from django.core.cache import cache

from cash.models import Direction, Exchange, City


def get_or_set_cash_directions_cache():
    '''
    Получить или установить кэш значение наличных направлений с городами
    '''

    if not (all_cash_directions := cache.get('all_cash_directions', False)):
        cash_directions = Direction.objects\
                                .select_related('valute_from', 'valute_to')\
                                .values_list('valute_from', 'valute_to').all()
        cities_for_parse = City.objects.filter(is_parse=True).all()
        all_cash_directions = set()
        for city in cities_for_parse:
            for valute_from, valute_to in cash_directions:
                all_cash_directions.add((city.code_name, valute_from, valute_to))
        cache.set('all_cash_directions', all_cash_directions, 60)
        print('SET VALUE TO CACHE')
    else:
        print('VALUE GETTING FROM CACHE')
    return all_cash_directions


def get_cash_direction_set_for_creating(directions: set[tuple[str,str,str]],
                                        exchange: Exchange):
    '''
    Получить перечень направлений для создания
    '''

    exchange_directions = exchange\
                            .directions\
                            .values_list('city', 'valute_from', 'valute_to').all()
    exchange_black_list_directions = exchange\
                                .direction_black_list\
                                .values_list('city', 'valute_from', 'valute_to').all()
    checked_directions_by_exchange = exchange_black_list_directions.union(exchange_directions)
    # print('ALL DIRECTION', all_cash_directions)
    # print('EXCHANGE DIRECTION', exchange_directions)
    # print('BLACK LIST', exchange_black_list_directions)
    # directions -= set(exchange_directions)
    # directions -= set(exchange_black_list_directions)
    directions -= set(checked_directions_by_exchange)
    print('DIRECTIONS FOR CREATING', directions)

    return directions


def generate_direction_dict(directions: tuple[str,str,str]):
    direction_dict = {}
    for city, valute_from, valute_to in directions:
        direction_dict[city] = direction_dict.get(city, []) + [(valute_from, valute_to)]

    return direction_dict
