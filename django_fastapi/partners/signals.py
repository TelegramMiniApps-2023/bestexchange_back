from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from general_models.utils.base import get_actual_datetime, UNIT_TIME_CHOICES
from general_models.utils.periodic_tasks import get_or_create_schedule
from general_models.models import PartnerTimeUpdate

from .models import Direction, Exchange, Review, Comment


# Сигнал для создания периодической задачи, которая проверяет
# партнёрские направления на активность, если направление не изменялось
# более 3 дней, направление становится неактивным
@receiver(post_save, sender=PartnerTimeUpdate)
def create_custom_user_for_user(sender, instance, created, **kwargs):
    if instance.name == 'Управление временем проверки активности направлений':
        if created:
            amount = instance.amount
            unit_time = instance.unit_time

            schedule = get_or_create_schedule(amount,
                                              UNIT_TIME_CHOICES[unit_time])
            PeriodicTask.objects.create(
                    interval=schedule,
                    name='check_update_time_for_directions_task',
                    task='check_update_time_for_directions',
                    )


#Сигнал для добавления поля en_name обменника
#перед созданием в БД
@receiver(pre_save, sender=Exchange)
def add_en_name_for_exchange(sender, instance, **kwargs):
    if not instance.en_name:
        instance.en_name = instance.name


#Сигнал для автоматической установки времени
#по московскому часовому поясу при создании отзыва в БД
@receiver(pre_save, sender=Review)
def change_time_create_for_review(sender, instance, **kwargs):
    if instance.time_create is None:
        instance.time_create = get_actual_datetime()


#Сигнал для автоматической установки времени
#по московскому часовому поясу при создании комментария в БД
@receiver(pre_save, sender=Comment)
def change_time_create_for_comment(sender, instance, **kwargs):
    if instance.time_create is None:
        instance.time_create = get_actual_datetime()


@receiver(pre_save, sender=Direction)
def change_time_create_for_direction(sender, instance, **kwargs):
    if instance.time_update is None:
        instance.time_update = get_actual_datetime()