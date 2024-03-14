from celery import shared_task, current_task
from celery.app.task import Task

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from cash import models as cash_models
from no_cash import models as no_cash_models
from partners import models as partner_models

from config import SELENIUM_DRIVER

from .utils.parse_reviews.selenium import parse_reviews


#Задача для периодического удаления отзывов и комментариев
#со статусом "Отклонён" из БД
@shared_task(name='delete_cancel_reviews')
def delete_cancel_reviews():
    cash_models.Review.objects.filter(status='Отклонён').delete()
    no_cash_models.Review.objects.filter(status='Отклонён').delete()
    partner_models.Review.objects.filter(status='Отклонён').delete()

    cash_models.Comment.objects.filter(status='Отклонён').delete()
    no_cash_models.Comment.objects.filter(status='Отклонён').delete()
    partner_models.Comment.objects.filter(status='Отклонён').delete()


#WITH SELENIUM
#Фоновая задача парсинга отзывов и комментариев
#для всех обменников из БД при запуске сервиса
@shared_task(acks_late=True, task_reject_on_worker_lost=True)
def parse_reviews_with_start_service():
    try:
        # driver = webdriver.Firefox()
        options = Options()
        driver = webdriver.Remote(f'http://{SELENIUM_DRIVER}:4444', options=options)

        for marker in ('no_cash', 'cash'):
            model = no_cash_models if marker == 'no_cash' else cash_models
            exchanges = model.Exchange.objects.values('en_name').all()
            exchange_name_list = [exchange['en_name'].lower() for exchange in exchanges]
            for exchange_name in exchange_name_list:
                parse_reviews(driver,
                              exchange_name,
                              marker)
    except (Exception, BaseException) as ex:
        print(ex)
    finally:
        driver.quit()


#Фоновая задача парсинга отзывов и комментариев обменника
#при добавлении обменника через админ панель
@shared_task(acks_late=True, task_reject_on_worker_lost=True)
def parse_reviews_for_exchange(exchange_name: str, marker: str):
    exchange_name = exchange_name.lower()

    options = Options()
    try:
        driver = webdriver.Remote(f'http://{SELENIUM_DRIVER}:4444', options=options)
        parse_reviews(driver, exchange_name, marker)
    except Exception as ex:
        print(ex)
    finally:
        driver.quit()


@shared_task(name='update_popular_count_direction_time')
def update_popular_count_direction():
    cash_direction = cash_models.Direction.objects.all()
    no_cash_directions = no_cash_models.Direction.objects.all()

    cash_direction.update(popular_count=0)
    no_cash_directions.update(popular_count=0)