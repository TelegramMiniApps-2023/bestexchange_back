import datetime

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from django_celery_beat.models import PeriodicTask

from .models import Valute
# from .periodic_tasks import (manage_periodic_task_for_create,
#                              manage_periodic_task_for_update,
#                              manage_periodic_task_for_parse_black_list)




#Сигнал для автоматической установки английского названия
#валюты(если оно не указано) при создании валюты в БД
@receiver(pre_save, sender=Valute)
def add_en_name_to_valute_obj(sender, instance, **kwargs):
    if instance.en_name is None:
        instance.en_name = instance.name