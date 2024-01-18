from django.core.management.base import BaseCommand, CommandError

from general_models.tasks import parse_reviews_with_start_service
from general_models.utils.parse_reviews.bs4 import get_exchange_list

from cash import models as cash_models
from no_cash import models as no_cash_models


# python manage.py parse_reviews_selenium
# В процессе запуска проекта использовать ТОЛЬКО ОДНУ из следующих команд:
# ЛИБО "python manage.py parse_reviews_bs4", ЛИБО "python manage.py parse_reviews_selenium" !!!


class Command(BaseCommand):
    print('Parse reviews for exchanges with Selenuim')

    def handle(self, *args, **kwargs):
        try:
            cash_exchange_list = cash_models.Exchange.objects.values('name').all()
            no_cash_exchange_list = no_cash_models.Exchange.objects.values('name').all()
            exchange_list = cash_exchange_list.union(no_cash_exchange_list)
            exchange_name_set = {exchange['name'].lower() for exchange in exchange_list}
            # print(exchange_name_set)
            # print(len(exchange_name_set))

            data_for_selenium = get_exchange_list(exchange_name_set)

            parse_reviews_with_start_service.delay(data_for_selenium)
            
        except Exception as ex:
            print(ex)
            raise CommandError('Initalization failed.')