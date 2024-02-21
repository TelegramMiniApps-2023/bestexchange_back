from django.core.management.base import BaseCommand, CommandError

from general_models.tasks import parse_reviews_with_start_service


# python manage.py parse_reviews_selenium
# В процессе запуска проекта использовать ТОЛЬКО ОДНУ из следующих команд:
# ЛИБО "python manage.py parse_reviews_bs4", ЛИБО "python manage.py parse_reviews_selenium" !!!


class Command(BaseCommand):
    print('Parse reviews for exchanges with Selenuim')

    def handle(self, *args, **kwargs):
        try:
            parse_reviews_with_start_service.delay()
            
        except Exception as ex:
            print(ex)
            raise CommandError('Initalization failed.')