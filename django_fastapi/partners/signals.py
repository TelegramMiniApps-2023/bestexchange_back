import datetime

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import Direction, Exchange, Review, Comment


#Сигнал для добавления поля en_name обменника
#перед созданием в БД
@receiver(pre_save, sender=Exchange)
def add_en_name_for_exchange(sender, instance, **kwargs):
    if not instance.en_name:
        instance.en_name = instance.name


#Сигнал для удаления дубликатов созданного направления
#(если такие есть)
# @receiver(pre_save, sender=Direction)
# def check_direction_on_unique(sender, instance, **kwargs):
#     exchange_id = instance.exchange_id
#     direction_id = instance.direction_id
#     cities_id = instance.cities_id

#     dublucate_direction = Exchange.objects.get(id=exchange_id)\
#                                     .directions.filter(direction_id=direction_id,
#                                                        cities_id=cities_id).all()

#     if dublucate_direction:
#         dublucate_direction.delete()


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