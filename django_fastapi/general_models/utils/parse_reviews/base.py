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
    
    exchange = exchange.objects.get(name__icontains=exchange_name)
    print('EXCHANGE!!!!!!!!!!!!!!!!!!!!!!')
    print(exchange)
    review = review(username=data['name'],
                    text=data['text'],
                    time_create=data['date'],
                    exchange=exchange,
                    status='Опубликован',
                    moderation=True)
    try:
        review.save()
    except Exception:
        pass
    return review


def new_add_review_to_db(exchange_name: str, data: dict, marker: str):
    match marker:
        case 'no_cash':
            exchange = no_cash_models.Exchange
            review = no_cash_models.Review
        case 'cash':
            exchange = cash_models.Exchange
            review = cash_models.Review
    
    exchange = exchange.objects.get(en_name__icontains=exchange_name)
    print('EXCHANGE!!!!!!!!!!!!!!!!!!!!!!')
    print(exchange)
    review = review(username=data['name'],
                    text=data['text'],
                    time_create=data['date'],
                    exchange=exchange,
                    status='Опубликован',
                    moderation=True)
    try:
        review.save()
    except Exception:
        pass
    # review.save()
    return review
    

def add_comment_to_db(review, data: dict, marker: str):
    match marker:
        case 'no_cash':
            comment = no_cash_models.Comment
        case 'cash':
            comment = cash_models.Comment
    try:
        comment.objects.create(username=data['name'],
                            text=data['text'],
                            time_create=data['date'],
                            review=review,
                            status='Опубликован',
                            moderation=True)
    except Exception:
        pass