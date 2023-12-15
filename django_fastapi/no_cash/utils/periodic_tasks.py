from no_cash.models import Exchange as NoCashExchange

from celery.local import Proxy


def run_no_cash_background_tasks(task: Proxy,
                                exchange: NoCashExchange,
                                direction_list: set,
                                xml_file: str):
    for direction in direction_list:
        valute_from_id, valute_to_id = direction
        dict_for_parse = exchange.__dict__.copy()
        dict_for_parse['valute_from_id'] = valute_from_id
        dict_for_parse['valute_to_id'] = valute_to_id
        if dict_for_parse.get('_state'):
            dict_for_parse.pop('_state')
        task.delay(dict_for_parse, xml_file)