from celery.local import Proxy

from cash.models import Exchange as CashExchange, BlackListElement, Direction, City
from .parsers import check_city_in_xml_file


def run_cash_background_tasks(task: Proxy,
                              exchange: CashExchange,
                              direction_dict: dict,
                              xml_file: str,
                              black_list_parse=False):
    '''
    Запуск фоновых задач для создания
    наличных готовых направлений
    '''

    for city in direction_dict:
        if not check_city_in_xml_file(city, xml_file):
            print(f'Нет города {city} в {exchange.name}')
            if not black_list_parse:
                for valute_from, valute_to in direction_dict[city]:
                    direction = Direction.objects.get(valute_from=valute_from,
                                                      valute_to=valute_to)
                    city_model = City.objects.get(code_name=city)
                    black_list_element, _ = BlackListElement\
                                            .objects\
                                            .get_or_create(city=city_model,
                                                           direction=direction)
                                            # .get_or_create(city=city,
                                            #                valute_from=valute_from,
                                            #                valute_to=valute_to)
                    try:
                        exchange.direction_black_list.add(black_list_element)
                    except Exception:
                        pass
        else:
            for direction in direction_dict[city]:
                valute_from_id, valute_to_id = direction
                dict_for_parse = exchange.__dict__.copy()
                dict_for_parse['valute_from_id'] = valute_from_id
                dict_for_parse['valute_to_id'] = valute_to_id
                dict_for_parse['city'] = city
                if dict_for_parse.get('_state'):
                    dict_for_parse.pop('_state')
                task.delay(dict_for_parse, xml_file)


def run_update_tasks(task: Proxy,
                     exchange: CashExchange,
                     direction_list: list,
                     xml_file: str):
    '''
    Запуск фоновых задач для обновления
    наличных готовых направлений
    '''

    for direction in direction_list:
        city, valute_from_id, valute_to_id = direction
        dict_for_parse = exchange.__dict__.copy()
        dict_for_parse['valute_from_id'] = valute_from_id
        dict_for_parse['valute_to_id'] = valute_to_id
        dict_for_parse['city'] = city
        if dict_for_parse.get('_state'):
            dict_for_parse.pop('_state')
        task.delay(dict_for_parse, xml_file)