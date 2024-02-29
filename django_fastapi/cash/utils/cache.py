from django.core.cache import cache

from cash.models import Direction, City


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