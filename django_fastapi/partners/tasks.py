import requests

from time import sleep

from celery import shared_task

from django.db.models import Q

from cash.models import Direction


@shared_task(name='parse_cash_courses')
def parse_cash_courses():
    limit_direction = Q(valute_from__type_valute='Криптовалюта',
                        valute_to__type_valute='Наличные') | \
                        Q(valute_from__type_valute='Наличные',
                            valute_to__type_valute='Криптовалюта')
    directions = Direction.objects\
                            .select_related('valute_from', 'valute_to')\
                            .filter(limit_direction).all()
    
    for direction in directions:
        valid_direction_name = direction.display_name.replace('CASH','')
        valute_from, valute_to = valid_direction_name.split(' -> ')
        try:
            resp = requests.get(
                f'https://api.coinbase.com/v2/prices/{valute_from}-{valute_to}/spot',
                timeout=5,
                )
        except Exception:
            continue
        else:
            try:
                json_resp = resp.json()
                actual_course = json_resp['data']['amount']
                print(valid_direction_name, actual_course)
                direction.actual_course = actual_course
                direction.save()
            except Exception:
                pass
        sleep(0.3)

