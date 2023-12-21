from celery import shared_task

from cash import models as cash_models
from no_cash import models as no_cash_models


#Задача для периодического удаления отзывов и комментариев
#со статусом "Отклонён" из БД
@shared_task(name='delete_cancel_reviews')
def delete_cancel_reviews():
    cash_models.Review.objects.filter(status='Отклонён').delete()
    no_cash_models.Review.objects.filter(status='Отклонён').delete()

    cash_models.Comment.objects.filter(status='Отклонён').delete()
    no_cash_models.Comment.objects.filter(status='Отклонён').delete()
    