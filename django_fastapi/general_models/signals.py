from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import Valute
from cash.models import CustomUser


#Сигнал для автоматической установки английского названия
#валюты(если оно не указано) при создании валюты в БД
@receiver(pre_save, sender=Valute)
def add_en_name_to_valute_obj(sender, instance, **kwargs):
    if instance.en_name is None:
        instance.en_name = instance.name


#Сигнал для создания корректного пользователя админ панели
@receiver(pre_save, sender=User)
def add_fields_for_user(sender, instance, **kwargs):
    if not instance.is_superuser:
        instance.is_active = True
        instance.is_staff = True


#Сигнал для создания связующей модели (пользователь + наличный обменник)
#при создании модели пользователя админ панели
@receiver(post_save, sender=User)
def create_custom_user_for_user(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser:
            CustomUser.objects.create(user=instance)