from datetime import datetime

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from no_cash import models as no_cash_models
from cash import models as cash_models


def add_review_to_db(exchange_name: str, data: dict, marker: str):
    match marker:
        case 'no_cash':
            exchange = no_cash_models.Exchange
            review = no_cash_models.Review
        case 'cash':
            exchange = cash_models.Exchange
            review = cash_models.Review
    # type_exchange = no_cash_models.Exchange if marker == 'no_cash' else cash_models.Exchange
    exchange = exchange.objects.get(name__icontains=exchange_name)
    # exchange = no_cash_models.Exchange.objects.filter(name__icontains=exchange_name)
    # if not exchange:
    #     exchange = cash_models.Exchange.objects.filter(name__icontains=exchange_name)

    # exchange = exchange.get()
    print('EXCHANGE!!!!!!!!!!!!!!!!!!!!!!')
    print(exchange)
    review = review(username=data['name'],
                    text=data['text'],
                    time_create=data['date'],
                    exchange=exchange)
    review.save()
    return review
    # review.objects.create(username=data['name'],
    #                       text=data['text'],
    #                       time_create=data['date'],
    #                       exchange=exchange)
    

def add_comment_to_db(review, data: dict, marker: str):
    match marker:
        case 'no_cash':
            comment = no_cash_models.Comment
        case 'cash':
            comment = cash_models.Comment

    comment.objects.create(username=data['name'],
                          text=data['text'],
                          time_create=data['date'],
                          review=review)


def collect_data(review, indicator: str):
    header = review.find_element(By.CLASS_NAME, f'{indicator}_header')\
                    .find_elements(By.TAG_NAME, 'td')
    if indicator == 'review':
        # _, name , _, _, date = tuple(map(lambda el: el.text, header))
        _, name , _, _, date = header
        date = date.find_element(By.TAG_NAME, 'span')
        # print(dir(date))
        w = date.get_attribute('title')
        print(w)

    else:
        # _, name, date = tuple(map(lambda el: el.text, header))
        _, name, date = header
        date = date.find_element(By.TAG_NAME, 'span')
        # print(dir(date))
        w = date.get_attribute('title')
        print(w)


    print(name.text)
    # print(date)
    # w = w.replace(' UTC', '')
    w = w[:20]
    date = datetime.strptime(w, '%d.%m.%Y, %H:%M:%S')
    print(date)
    rate_text = review.find_element(By.CLASS_NAME, f'{indicator}_middle')\
                        .find_element(By.CLASS_NAME, f'{indicator}_text')
    print(rate_text.text)

    return {
        'name': name.text,
        'date': date,
        'text': rate_text.text,
    }


def parse_review(driver,
                 exchange_data: tuple[str, str],
                 marker: str,
                 limit: int = 20):
    exchange_name, link = exchange_data
    try:
        # service = Service(port=4442)
        # options = Options()
        # driver = webdriver.Remote('http://localhost:4444', options=options)
        # driver = webdriver.Remote(f'http://{SELENUIM_DRIVER}:4444', options=options)

        # driver = webdriver.Firefox()
        # driver.get(f'https://www.bestchange.ru/{exchange_name.lower()}-exchanger.html')
        driver.get(link)

        rates = driver.find_element(By.ID, 'content_reviews')\
                        .find_element(By.CLASS_NAME, 'inner')\
                        .find_elements(By.XPATH, '//div[starts-with(@class, "review_block")]')          
        print(len(rates))

        for rate in rates[:limit]:
            try:
                data = collect_data(rate, 'review')
            except ValueError as ex:
                print(ex)
                continue
            else:
                review = add_review_to_db(exchange_name, data, marker)

            comments = rate.find_element(By.CLASS_NAME, 'review_comment_expand')

            print(comments.is_displayed())

            if comments.is_displayed():
                comments.click()
                comments = rate.find_elements(By.CLASS_NAME, 'review_comment')
                for comment in comments:
                    try:
                        data = collect_data(comment, 'comment')
                    except ValueError:
                        continue
                    else:
                        add_comment_to_db(review, data, marker)
    except Exception as ex:
        print(ex)
        driver.close()
    # except NoSuchElementException:
    #     print('ERROR')
    # finally:
    #     driver.quit()