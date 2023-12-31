from celery import shared_task

from general_models.utils.exc import NoFoundXmlElement
from general_models.utils.periodic_tasks import try_get_xml_file
from .utils.parsers import cash_parse_xml
from .utils.periodic_tasks import run_cash_background_tasks, run_update_tasks
from .utils.tasks import (get_or_set_cash_directions_cache,
                          get_cash_direction_set_for_creating,
                          generate_direction_dict)

from .models import Exchange, ExchangeDirection, BlackListElement


#PERIODIC CREATE
@shared_task(name='create_cash_directions_for_exchange')
def create_cash_directions_for_exchange(exchange_name: str):
    exchange = Exchange.objects.get(name=exchange_name)
    xml_file = try_get_xml_file(exchange)
    
    if xml_file is not None:
        if exchange.is_active:
            all_cash_directions = get_or_set_cash_directions_cache()
            direction_list = get_cash_direction_set_for_creating(all_cash_directions,
                                                                 exchange)

            if direction_list:
                direction_dict = generate_direction_dict(direction_list)
                run_cash_background_tasks(create_direction,
                                          exchange,
                                          direction_dict,
                                          xml_file)


@shared_task
def create_direction(dict_for_parse: dict,
                     xml_file: str):
    print('*' * 10)
    print('inside task')

    try:
        dict_for_create_exchange_direction = cash_parse_xml(dict_for_parse, xml_file)
    except NoFoundXmlElement:
        black_list_element, _ = BlackListElement\
                                .objects\
                                .get_or_create(city=dict_for_parse['city'],
                                                valute_from=dict_for_parse['valute_from_id'],
                                                valute_to=dict_for_parse['valute_to_id'])
        print('Нет элемента')
        Exchange.objects.get(name=dict_for_parse['name'])\
                        .direction_black_list.add(black_list_element)
    except Exception as ex:
        print('PARSE FAILED', ex)
        pass
    else:
        print('Получилось')
        exchange = Exchange.objects.get(name=dict_for_parse['name'])
        dict_for_create_exchange_direction['exchange'] = exchange
        try:
            ExchangeDirection.objects.create(**dict_for_create_exchange_direction)
        except Exception:
            pass


#PERIODIC UPDATE
@shared_task(name='update_cash_directions_for_exchange')
def update_cash_directions_for_exchange(exchange_name: str):
    exchange = Exchange.objects.get(name=exchange_name)
    xml_file = try_get_xml_file(exchange)

    if xml_file is not None:
        if exchange.is_active:
            direction_list = exchange\
                            .directions\
                            .values_list('city', 'valute_from', 'valute_to').all()

            if direction_list:
                run_update_tasks(try_update_direction,
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
                                    city=dict_for_parse['city'],
                                    valute_from=dict_for_parse['valute_from_id'],
                                    valute_to=dict_for_parse['valute_to_id'],
                                    )
        dict_for_update_exchange_direction = cash_parse_xml(dict_for_parse, xml_file)
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
@shared_task(name='try_create_cash_directions_from_black_list')
def try_create_cash_directions_from_black_list(exchange_name: str):
    exchange = Exchange.objects.get(name=exchange_name)
    xml_file = try_get_xml_file(exchange)

    if xml_file is not None:
        if exchange.is_active:
            black_list_directions = exchange.direction_black_list\
                                            .values_list('city', 'valute_from', 'valute_to').all()

            if black_list_directions:
                direction_dict = generate_direction_dict(black_list_directions)
                run_cash_background_tasks(try_create_black_list_direction,
                                          exchange,
                                          direction_dict,
                                          xml_file,
                                          black_list_parse=True)


@shared_task
def try_create_black_list_direction(dict_for_parse: dict,
                                    xml_file: str):
    print('*' * 10)
    print('inside task')

    try:
        dict_for_exchange_direction = cash_parse_xml(dict_for_parse, xml_file)
    except Exception as ex:
        print('BLACK LIST PARSE FAILED', ex)
        pass
    else:
        exchange = Exchange.objects.get(name=dict_for_parse['id'])
        dict_for_exchange_direction['exchange'] = exchange
        try:
            ExchangeDirection.objects.create(**dict_for_exchange_direction)

            black_list_element = BlackListElement.objects\
                                    .get(city=dict_for_exchange_direction['city'],
                                    valute_from=dict_for_exchange_direction['valute_from'],
                                    valute_to=dict_for_exchange_direction['valute_to'])
            exchange.direction_black_list.remove(black_list_element)
        except Exception:
            pass