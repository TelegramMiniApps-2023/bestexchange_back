from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from .base import add_comment_to_db, new_add_review_to_db


def collect_data(review, indicator: str):
    header = review.find_element(By.CLASS_NAME, f'{indicator}_header')\
                    .find_elements(By.TAG_NAME, 'td')
    
    if indicator == 'review':
        _, name , _, _, date = header
    else:
        _, name, date = header
    
    date = date.find_element(By.TAG_NAME, 'span')
    date_string = date.get_attribute('title') # строка в формате "xx.xx.xxxx, xx:xx:xx"

    print(name.text)

    valid_date_format = date_string[:20]
    date = datetime.strptime(valid_date_format, '%d.%m.%Y, %H:%M:%S')
    print(date)
    rate_text = review.find_element(By.CLASS_NAME, f'{indicator}_middle')\
                        .find_element(By.CLASS_NAME, f'{indicator}_text')
    print(rate_text.text)

    return {
        'name': name.text,
        'date': date,
        'text': rate_text.text,
    }


def parse_reviews(driver: WebDriver,
                  exchange_name: str,
                  marker: str,
                  limit: int = 20):
    link = f'https://www.bestchange.ru/{exchange_name}-exchanger.html'
    try:
        driver.get(link)

        rows = driver.find_element(By.ID, 'content_reviews')\
                        .find_element(By.CLASS_NAME, 'inner')\
                        .find_elements(By.XPATH, '//div[starts-with(@class, "review_block")]')          
        print(len(rows))

        for row in rows[:limit]:
            try:
                data = collect_data(row, 'review')
            except ValueError as ex:
                print(ex)
                continue
            else:
                review = new_add_review_to_db(exchange_name, data, marker)
##
                comments = row.find_element(By.CLASS_NAME, 'review_comment_expand')

                print(comments.is_displayed())

                if comments.is_displayed():
                    comments.click()
                    comments = row.find_elements(By.CLASS_NAME, 'review_comment')
                    for comment in comments:
                        try:
                            data = collect_data(comment, 'comment')
                        except ValueError:
                            continue
                        else:
                            add_comment_to_db(review, data, marker)
    except Exception as ex:
        print(ex)
    except BaseException as ex:
        print(ex)
        return