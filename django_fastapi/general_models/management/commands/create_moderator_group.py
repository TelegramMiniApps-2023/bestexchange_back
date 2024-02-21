from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission

from partners.models import Exchange, Direction, Review, Comment, PartnerCity


class Command(BaseCommand):
    print('Creating Group Partners')

    def handle(self, *args, **kwargs):
        try:
            moderator_group, _ = Group.objects.get_or_create(name='Партнёры')
            
            for model in (Exchange, Direction, Review, Comment, PartnerCity):
                content_type = ContentType.objects.get_for_model(model)
                permissions = Permission.objects.filter(content_type=content_type)
                moderator_group.permissions.add(*permissions)
        except Exception as ex:
            print(ex)
            raise CommandError('Initalization failed.')