from django.db import models

from general_models.models import BaseExchange, BaseReview, BaseComment

from cash.models import Direction as CashDirection, City


class Exchange(BaseExchange):
    
    class Meta:
        verbose_name = 'Обменник'
        verbose_name_plural = 'Обменники'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['en_name']),
        ]


class Direction(models.Model):
    exchange = models.ForeignKey(Exchange,
                                 verbose_name='Обменник',
                                 on_delete=models.CASCADE)
    direction = models.ForeignKey(CashDirection,
                                  verbose_name='Направление',
                                  on_delete=models.CASCADE,
                                  related_name='partner_directions')
    cities = models.ManyToManyField(City,
                                    verbose_name='Города')
    percent = models.FloatField(default=0)
    fix_amount = models.FloatField(default=0)


    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'


class Review(BaseReview):
    exchange = models.ForeignKey(Exchange,
                                 on_delete=models.CASCADE,
                                 verbose_name='Наличный обменник',
                                 related_name='reviews')
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-time_create', 'status', 'exchange')

    def __str__(self):
        return 'Партнёрский ' + super().__str__()


class Comment(BaseComment):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               verbose_name='Отзыв',
                               related_name='comments')
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-time_create', 'status', 'review')

    def __str__(self):
        return 'Партнёрский ' + super().__str__()