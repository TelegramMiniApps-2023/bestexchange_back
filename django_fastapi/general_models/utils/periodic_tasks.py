import re
import requests

from xml.etree import ElementTree as ET

from django_celery_beat.models import IntervalSchedule

from general_models.models import BaseExchange

from .exc import RobotCheckError


def get_or_create_schedule(interval: int, period: str):
    '''
    Получить или создать расписание для периодической задачи в БД
    '''
    schedule, _ = IntervalSchedule.objects.get_or_create(
                            every=interval,
                            period=period,
                        )
    return schedule
   

def try_get_xml_file(exchange: BaseExchange) -> str | None:
    '''
    Возвращает XML файл в формате строки или None
    '''
    
    try:
        is_active, xml_file = request_to_xml_file(exchange.xml_url)
    except Exception as ex:
        print('CHECK ACTIVE EXCEPTION!!!', ex)
        if exchange.is_active:
            exchange.is_active = False
            exchange.save()
    else:
        if exchange.period_for_update != 0:
            if exchange.is_active != is_active:
                exchange.is_active = is_active
                exchange.save()
            return xml_file


def request_to_xml_file(xml_url: str):
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'My User Agent 1.0',
    })
    resp = requests.get(xml_url,
                        headers=headers,
                        timeout=5) #можно меньше
    content_type = resp.headers['Content-Type']

    if not re.match(r'^[a-zA-Z]+\/xml?', content_type):
        raise RobotCheckError(f'{xml_url} требует проверку на робота')
    else:
        xml_file = resp.text
        print(xml_url)
        root = ET.fromstring(xml_file)
        is_active = True
        if root.text == 'Техническое обслуживание':
            is_active = False
        return (is_active, xml_file)