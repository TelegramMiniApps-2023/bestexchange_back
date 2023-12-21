import datetime

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from django_celery_beat.models import PeriodicTask

from .models import Exchange, Direction, ExchangeDirection, Review, Comment
from .periodic_tasks import (manage_periodic_task_for_create,
                             manage_periodic_task_for_update,
                             manage_periodic_task_for_parse_black_list)


#Сигнал для удаления всех связанных готовых направлений
#при удалении направления из БД
@receiver(post_delete, sender=Direction)
def delete_directions_from_exchanges(sender, instance, **kwargs):
    direction_list = ExchangeDirection.objects.filter(valute_from=instance.valute_from,
                                                      valute_to=instance.valute_to).all()
    direction_list.delete()


#Сигнал для создания периодических задач
#при создании обменника в БД
@receiver(post_save, sender=Exchange)
def create_tasks_for_exchange(sender, instance, created, **kwargs):
    if created:
        print('NO CASH PERIODIC TASKS CREATING...')
        manage_periodic_task_for_create(instance.name,
                                        instance.period_for_create)
        manage_periodic_task_for_update(instance.name,
                                        instance.period_for_update)
        manage_periodic_task_for_parse_black_list(instance.name,
                                                  instance.period_for_parse_black_list)


#Сигнал для удаления периодических задач
#при удалении обменника из БД
@receiver(post_delete, sender=Exchange)
def delete_task_for_exchange(sender, instance, **kwargs):
    PeriodicTask.objects.filter(name__startswith=f'{instance.name} no_cash').delete()


#Сигнал для автоматической установки времени
#по московскому часовому поясу при создании отзыва в БД
@receiver(pre_save, sender=Review)
def change_time_create_for_review(sender, instance, **kwargs):
    if instance.time_create is None:
        instance.time_create = datetime.datetime.now() + datetime.timedelta(hours=9)


#Сигнал для автоматической установки времени
#по московскому часовому поясу при создании комментария в БД
@receiver(pre_save, sender=Comment)
def change_time_create_for_comment(sender, instance, **kwargs):
    if instance.time_create is None:
        instance.time_create = datetime.datetime.now() + datetime.timedelta(hours=9)
