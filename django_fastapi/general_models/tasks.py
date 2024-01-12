from celery import shared_task

from .utils.selenium import parse_review

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
    

# @shared_task
# def parse_reviews_with_start_service(*exchange_names):
#     for idx, exchange_name in enumerate(exchange_names, start=1):
#         print('*' * 10)
#         print(idx)
#         print(exchange_name)
#         parse_review(exchange_name)
    

@shared_task
def parse_reviews_with_start_service(data_for_selenium: dict):
    for marker in ('no_cash', 'cash'):
        model = no_cash_models if marker == 'no_cash' else cash_models
        exchanges = model.Exchange.objects.values('name').all()
        exchange_name_list = [exchange['name'].lower() for exchange in exchanges]
        for exchange in exchange_name_list:
            if exchange in data_for_selenium:
                parse_review((exchange, data_for_selenium[exchange]), marker)
    # no_cash_exchanges = no_cash_models.Exchange.objects.values('name').all()
    # no_cash_exchange_name_list = [exchange['name'].lower() for exchange in no_cash_exchanges]
    # marker = 'no_cash'
    # for exchange in no_cash_exchange_name_list:
    #     if exchange in data_for_selenium:
    #         parse_review((exchange, data_for_selenium[exchange]), marker)
    # for idx, exchange_name in enumerate(exchange_names, start=1):
    #     print('*' * 10)
    #     print(idx)
    #     print(exchange_name)
    #     parse_review(exchange_name)