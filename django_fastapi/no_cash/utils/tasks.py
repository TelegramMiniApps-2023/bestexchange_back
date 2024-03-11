from no_cash.models import Exchange


def get_no_cash_direction_set_for_creating(directions: set[tuple[str,str]],
                                           exchange: Exchange):
    '''
    Получить перечень направлений для создания
    '''

    # exchange_directions = exchange.directions\
    #                             .values_list('valute_from', 'valute_to').all()
    exchange_directions = exchange.directions\
                                .select_related('direction',
                                                'direction__valute_from',
                                                'direction__valute_to')\
                                .values_list('direction__valute_from',
                                             'direction__valute_to').all()

    # exchange_black_list_directions = exchange.direction_black_list\
    #                             .values_list('valute_from', 'valute_to').all()
    exchange_black_list_directions = exchange.direction_black_list\
                                .select_related('valute_from',
                                                'valute_to')\
                                .values_list('valute_from',
                                             'valute_to').all()
                                # .select_related('direction',
                                #                 'direction__valute_from',
                                #                 'direction__valute_to')\
                                # .values_list('direction__valute_from',
                                #              'direction__valute_to').all()

    checked_directions_by_exchange = exchange_black_list_directions.union(exchange_directions)

    directions -= set(checked_directions_by_exchange)
    print('DIRECTION FOR CREATING', directions)
    return directions