import datetime

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from django_celery_beat.models import PeriodicTask

from .models import Exchange, Direction, ExchangeDirection, Review, Comment
from .periodic_tasks import (manage_periodic_task_for_create,
                             manage_periodic_task_for_update,
                             manage_periodic_task_for_parse_black_list)


#Signal to delete all related direction records
@receiver(post_delete, sender=Direction)
def delete_directions_from_exchanges(sender, instance, **kwargs):
    direction_list = ExchangeDirection.objects.filter(valute_from=instance.valute_from,
                                                      valute_to=instance.valute_to).all()
    direction_list.delete()


#Signal to create periodic task for exchange
@receiver(post_save, sender=Exchange)
def create_tasks_for_exchange(sender, instance, created, **kwargs):
    if created:
        print('CASH PERIODIC TASKS CREATING...')
        manage_periodic_task_for_create(instance.name,
                                        instance.period_for_create)
        manage_periodic_task_for_update(instance.name,
                                        instance.period_for_update)
        manage_periodic_task_for_parse_black_list(instance.name,
                                                  instance.period_for_parse_black_list)


#Signal to delete related periodic task for Exchange
@receiver(post_delete, sender=Exchange)
def delete_task_for_exchange(sender, instance, **kwargs):
    PeriodicTask.objects.filter(name__startswith=f'{instance.name} cash').delete()


@receiver(pre_save, sender=Review)
def change_time_create_for_review(sender, instance, **kwargs):
    if instance.time_create is None:
        instance.time_create = datetime.datetime.now() + datetime.timedelta(hours=9)


@receiver(pre_save, sender=Comment)
def change_time_create_for_comment(sender, instance, **kwargs):
    if instance.time_create is None:
        instance.time_create = datetime.datetime.now() + datetime.timedelta(hours=9)