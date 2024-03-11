from xml.etree import ElementTree as ET

from general_models.utils.exc import NoFoundXmlElement
from general_models.utils.tasks import make_valid_values_for_dict


def no_cash_parse_xml(dict_for_parser: dict,
                      xml_file: str):
        direction_dict = dict_for_parser.copy()
        valute_from = direction_dict.pop('valute_from_id')
        valute_to = direction_dict.pop('valute_to_id')

        xml_url = dict_for_parser.get('xml_url')
        root = ET.fromstring(xml_file)

        element = root.find(f'item[from="{valute_from}"][to="{valute_to}"]')

        if element is not None:
            dict_for_exchange_direction = {
                # 'valute_from': valute_from,
                # 'valute_to': valute_to,
                'in_count': element.find('in').text,
                'out_count': element.find('out').text,
                'min_amount': element.find('minamount').text,
                'max_amount': element.find('maxamount').text
                }
            make_valid_values_for_dict(dict_for_exchange_direction)
            return dict_for_exchange_direction
        else:
            raise NoFoundXmlElement(f'Xml элемент не найден, {xml_url}')