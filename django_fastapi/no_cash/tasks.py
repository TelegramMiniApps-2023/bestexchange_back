from celery import shared_task


from general_models.utils.exc import NoFoundXmlElement
from general_models.utils.periodic_tasks import try_get_xml_file
from .utils.periodic_tasks import run_no_cash_background_tasks
from .utils.parsers import no_cash_parse_xml
from .utils.tasks import (get_or_set_no_cash_directions_cache,
                          get_no_cash_direction_set_for_creating)
from .models import Exchange, ExchangeDirection, Direction


#PERIODIC CREATE
@shared_task(name='create_no_cash_directions_for_exchange')
def create_no_cash_directions_for_exchange(exchange_name: str):
    exchange = Exchange.objects.get(name=exchange_name)
    xml_file = try_get_xml_file(exchange)
    
    if xml_file is not None and exchange.is_active:
            all_no_cash_directions = get_or_set_no_cash_directions_cache()
            direction_list = get_no_cash_direction_set_for_creating(all_no_cash_directions,
                                                                    exchange)
            if direction_list:
                run_no_cash_background_tasks(create_direction,
                                             exchange,
                                             direction_list,
                                             xml_file)


@shared_task
def create_direction(dict_for_parse: dict,
                     xml_file: str):
    print('*' * 10)
    print('inside task')

    try:
        dict_for_create_exchange_direction = no_cash_parse_xml(dict_for_parse, xml_file)
    except NoFoundXmlElement:
        not_found_direction = Direction.objects.get(valute_to=dict_for_parse['valute_to_id'],
                                                    valute_from=dict_for_parse['valute_from_id'])
        print('NOT FOUND DIRECTION', not_found_direction)
        Exchange.objects.get(name=dict_for_parse['name'])\
                        .direction_black_list.add(not_found_direction)
    except Exception as ex:
        print('PARSE FAILED', ex)
        pass
    else:
        # print('ДОБАВЛЯЮ')
        exchange = Exchange.objects.get(name=dict_for_parse['name'])
        dict_for_create_exchange_direction['exchange'] = exchange
        try:
            ExchangeDirection.objects.create(**dict_for_create_exchange_direction)
        except Exception as ex:
            print(ex)
            pass


#PERIODIC UPDATE
@shared_task(name='update_no_cash_diretions_for_exchange')
def update_no_cash_diretions_for_exchange(exchange_name: str):
    exchange = Exchange.objects.get(name=exchange_name)
    xml_file = try_get_xml_file(exchange)

    if xml_file is not None:
        if exchange.is_active:
            direction_list = exchange.directions.values_list('valute_from', 'valute_to').all()

            if direction_list:
                run_no_cash_background_tasks(try_update_direction,
                                             exchange,
                                             direction_list,
                                             xml_file)


@shared_task
def try_update_direction(dict_for_parse: dict,
                         xml_file: str):
    print('*' * 10)
    print('inside task')

    try:
        exchange_direction = ExchangeDirection.objects\
                            .filter(exchange=dict_for_parse['id'],
                            valute_from=dict_for_parse['valute_from_id'],
                            valute_to=dict_for_parse['valute_to_id'],
                            )
        dict_for_update_exchange_direction = no_cash_parse_xml(dict_for_parse, xml_file)
    except NoFoundXmlElement as ex:
        print('CATCH EXCEPTION', ex)
        exchange_direction.update(is_active=False)
        pass
    except Exception as ex:
        print('PARSE UPDATE FAILED', ex)
        pass
    else:
        print('update')
        dict_for_update_exchange_direction['is_active'] = True

        exchange_direction.update(**dict_for_update_exchange_direction)


#PERIODIC BLACK LIST
@shared_task(name='try_create_no_cash_directions_from_black_list')
def try_create_no_cash_directions_from_black_list(exchange_name: str):
    exchange = Exchange.objects.get(name=exchange_name)
    xml_file = try_get_xml_file(exchange)
    
    if xml_file is not None:
        if exchange.is_active:
            black_list_directions = exchange.direction_black_list\
                                            .values_list('valute_from', 'valute_to').all()

            if black_list_directions:
                run_no_cash_background_tasks(try_create_black_list_direction,
                                             exchange,
                                             black_list_directions,
                                             xml_file)


@shared_task
def try_create_black_list_direction(dict_for_parse: dict,
                                    xml_file: str):
    print('*' * 10)
    print('inside task')

    try:
        dict_for_exchange_direction = no_cash_parse_xml(dict_for_parse, xml_file)
    except NoFoundXmlElement as ex:
        print('CATCH EXCEPTION', ex)
        pass
    except Exception as ex:
        print('BLACK LIST PARSE FAILED', ex)
        pass
    else:
        exchange = Exchange.objects.get(name=dict_for_parse['name'])
        dict_for_exchange_direction['exchange'] = exchange
        try:
            ExchangeDirection.objects.create(**dict_for_exchange_direction)

            direction = Direction.objects\
                        .get(valute_from=dict_for_exchange_direction['valute_from'],
                             valute_to=dict_for_exchange_direction['valute_to'])
            exchange.direction_black_list.remove(direction)
        except Exception:
            pass