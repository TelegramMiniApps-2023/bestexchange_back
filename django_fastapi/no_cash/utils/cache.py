from django.core.cache import cache

from no_cash.models import Direction


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