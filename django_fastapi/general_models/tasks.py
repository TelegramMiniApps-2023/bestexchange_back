from time import sleep

from celery import shared_task

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.options import Options

from .utils.parse_reviews.selenium import parse_reviews
from .utils.parse_reviews.bs4 import get_exchange_list

from cash import models as cash_models
from no_cash import models as no_cash_models
from partners import models as partner_models

from config import SELENIUM_DRIVER


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
# @shared_task
# def parse_reviews_with_start_service(data_for_selenium: dict):
#     try:
#         # driver = webdriver.Firefox()
#         options = Options()
#         # driver = webdriver.Remote('http://localhost:4444', options=options)
#         driver = webdriver.Remote(f'http://{SELENIUM_DRIVER}:4444', options=options)

#         for marker in ('no_cash', 'cash'):
#             model = no_cash_models if marker == 'no_cash' else cash_models
#             exchanges = model.Exchange.objects.values('name').all()
#             exchange_name_list = [exchange['name'].lower() for exchange in exchanges]
#             for exchange_name in exchange_name_list:
#                 if exchange_name in data_for_selenium:
#                     parse_reviews(driver,
#                                   (exchange_name, data_for_selenium[exchange_name]),
#                                   marker)
#     except Exception as ex:
#         print(ex)
#         driver.quit()
#     finally:
#         driver.quit()


#WITH SELENIUM
#Фоновая задача парсинга отзывов и комментариев
#для всех обменников из БД при запуске сервиса
@shared_task
def parse_reviews_with_start_service():
    try:
        # driver = webdriver.Firefox()
        options = Options()
        # driver = webdriver.Remote('http://localhost:4444', options=options)
        driver = webdriver.Remote(f'http://{SELENIUM_DRIVER}:4444', options=options)

        for marker in ('no_cash', 'cash'):
            model = no_cash_models if marker == 'no_cash' else cash_models
            exchanges = model.Exchange.objects.values('en_name').all()
            exchange_name_list = [exchange['en_name'].lower() for exchange in exchanges]
            for exchange_name in exchange_name_list:
                parse_reviews(driver,
                              exchange_name,
                              marker)
    except Exception as ex:
        print(ex)
    finally:
        driver.quit()


#WITH BeautifulSoup
#Фоновая задача парсинга отзывов всех обменников из БД
#при запуске сервиса
# @shared_task
# def parse_reviews_with_start_service(data_for_selenium: dict):
#     for marker in ('no_cash', 'cash'):
#         model = no_cash_models if marker == 'no_cash' else cash_models
#         exchanges = model.Exchange.objects.values('name').all()
#         exchange_name_list = [exchange['name'].lower() for exchange in exchanges]
#         for exchange in exchange_name_list:
#             if exchange in data_for_selenium:
#                 parse_reviews((exchange, data_for_selenium[exchange]), marker)
#                 sleep(3)


#Фоновая задача парсинга отзывов и комментариев обменника
#при добавлении обменника через админ панель
# @shared_task
# def parse_reviews_for_exchange(exchange_name: str, marker: str):
#     exchange_name = exchange_name.lower()
#     data_for_selenium = get_exchange_list(set([exchange_name]))
#     print(data_for_selenium)

#     options = Options()
#     try:
#         driver = webdriver.Remote(f'http://{SELENIUM_DRIVER}:4444', options=options)
#         if exchange_name in data_for_selenium:
#             parse_reviews(driver, (exchange_name, data_for_selenium[exchange_name]), marker)
#     except Exception as ex:
#         print(ex)
#     finally:
#         driver.quit()


#Фоновая задача парсинга отзывов и комментариев обменника
#при добавлении обменника через админ панель
@shared_task
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