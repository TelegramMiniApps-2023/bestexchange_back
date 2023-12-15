from django.db import models
from django.core.exceptions import ValidationError

from general_models.models import (BaseExchangeDirection,
                                   Valute,
                                   BaseExchange,
                                   BaseDirection,
                                   BaseReview,
                                   BaseComment)


class Country(models.Model):
    name = models.CharField('Название страны', max_length=100, primary_key=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ('name', )

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField('Название города', max_length=100, primary_key=True)
    code_name = models.CharField('Кодовое имя', max_length=10, unique=True)
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE,
                                verbose_name='Страна',
                                related_name='cities')
    is_parse = models.BooleanField('Статус парсинга', default=False)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['is_parse', 'name']

    def __str__(self):
        return self.name

    
class Exchange(BaseExchange):
    direction_black_list = models.ManyToManyField('BlackListElement',
                                                  verbose_name='Чёрный список')
    

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
        return 'Наличный ' + super().__str__()


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
        return 'Наличный ' + super().__str__()


class Direction(BaseDirection):
    valute_from = models.ForeignKey(Valute,
                                    to_field='code_name',
                                    on_delete=models.CASCADE,
                                    verbose_name='Отдаём',
                                    related_name='cash_valutes_from')
    valute_to = models.ForeignKey(Valute,
                                  to_field='code_name',
                                  on_delete=models.CASCADE,
                                  verbose_name='Получаем',
                                  related_name='cash_valutes_to')
    
    def clean(self) -> None:
        if self.valute_from.type_valute == self.valute_to.type_valute:
            raise ValidationError('Значения "Отдаём" и "Получаем" должны иметь разные типы валют')
        
        if not 'Наличные' in (self.valute_from.type_valute, self.valute_to.type_valute):
            raise ValidationError('Одно из значений "Отдаём" и "Получаем" должно иметь наличный тип валюты, другое - безналичный')


class ExchangeDirection(BaseExchangeDirection):
    exchange = models.ForeignKey(Exchange,
                                 on_delete=models.CASCADE,
                                 verbose_name='Обменник',
                                 related_name='directions')
    city = models.CharField('Город', max_length=100)
    fromfee = models.FloatField('Процент', blank=True, null=True)
    params = models.CharField('Параметры', max_length=100, blank=True, null=True)

    class Meta:
        unique_together = (("exchange", "city", "valute_from", "valute_to"), )
        verbose_name = 'Готовое направление'
        verbose_name_plural = 'Готовые направления'
        ordering = ['-is_active', 'exchange', 'city', 'valute_from', 'valute_to']

    def __str__(self):
        return f'{self.city}: {self.valute_from} -> {self.valute_to}'


class BlackListElement(models.Model):
    city = models.CharField('Город', max_length=100)
    valute_from = models.CharField('Отдаём', max_length=10)
    valute_to = models.CharField('Получаем', max_length=10)

    class Meta:
        verbose_name = 'Элемент чёрного списка'
        verbose_name_plural = 'Элементы чёрного списка'
        unique_together = (("city",  "valute_from", "valute_to"), )
        ordering = ['city', 'valute_from', 'valute_to']

    def __str__(self):
        return f'({self.city}): {self.valute_from} -> {self.valute_to}\n\n'