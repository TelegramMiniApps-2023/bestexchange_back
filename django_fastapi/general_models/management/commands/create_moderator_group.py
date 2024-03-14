from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission

from general_models.utils.groups import create_group

from partners.models import Exchange, Direction, Review, Comment, PartnerCity

from seo_admin.models import SimplePage, FAQCategory, FAQPage

# python manage.py create_moderator_group в docker-compose файле
# Команда для создания группы "Партнёры" с ограниченными правами доступа


class Command(BaseCommand):
    print('Creating Group Partners')

    def handle(self, *args, **kwargs):
        try:
            create_group(group_name='Партнёры',
                         models=(Exchange, Direction, Review, Comment, PartnerCity))

            create_group(group_name='SEO админ',
                         models=(SimplePage, FAQCategory, FAQPage))

        except Exception as ex:
            print(ex)
            raise CommandError('Initalization failed.')