import datetime

from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from .models import Direction, Exchange, Review, Comment


#Сигнал для удаления дубликатов созданного направления
#(если такие есть)
@receiver(pre_save, sender=Direction)
def check_direction_on_unique(sender, instance, **kwargs):
    exchange_id = instance.exchange_id
    direction_id = instance.direction_id
    # final_amount = instance.final_amount

    # if final_amount < 1:
    #     k = 1 / final_amount
    #     in_count = k
    #     out_count = 1
    # else:
    #     in_count = 1
    #     out_count = final_amount

    # instance.in_count = in_count
    # instance.out_count = out_count

    dublucate_direction = Exchange.objects.get(id=exchange_id)\
                                    .directions.filter(direction_id=direction_id).all()

    if dublucate_direction:
        dublucate_direction.delete()


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