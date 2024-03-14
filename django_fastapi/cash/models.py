from django.db import models
from django.core.exceptions import ValidationError

from general_models.models import (BaseExchangeDirection,
                                   Valute,
                                   ParseExchange,
                                   BaseDirection,
                                   BaseReview,
                                   BaseComment)


#Модель страны
class Country(models.Model):
    name = models.CharField('Название страны(ru)', max_length=100,
                            unique=True)
    en_name = models.CharField('Название страны(en)', max_length=100,
                               unique=True)
    icon_url = models.FileField('Флаг страны',
                                upload_to='icons/country/',
                                blank=True,
                                null=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ('name', )
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['en_name'])
        ]

    def __str__(self):
        return self.name


#Модель города
class City(models.Model):
    name = models.CharField('Название города(ru)',
                            max_length=100,
                            unique=True)
    en_name = models.CharField('Название города(en)',
                               max_length=100,
                               unique=True)
    code_name = models.CharField('Кодовое имя',
                                 max_length=10,
                                 unique=True)
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE,
                                verbose_name='Страна',
                                related_name='cities')
    is_parse = models.BooleanField('Статус парсинга', default=False)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

        indexes = [
            models.Index(fields=['code_name', ])
        ]

    def __str__(self):
        return self.name


#Модель обменника    
class Exchange(ParseExchange):
    direction_black_list = models.ManyToManyField('BlackListElement',
                                                  verbose_name='Чёрный список')
    

#Модель отзыва
class Review(BaseReview):
    exchange = models.ForeignKey(Exchange,
                                 on_delete=models.CASCADE,
                                 verbose_name='Наличный обменник',
                                 related_name='reviews')
    
    class Meta:
        unique_together = (('exchange','username','time_create'), )
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-time_create', 'status', 'exchange')

    def __str__(self):
        return 'Наличный ' + super().__str__()


#Модель комментария
class Comment(BaseComment):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               verbose_name='Отзыв',
                               related_name='comments')
    
    class Meta:
        unique_together = (('review','username','time_create'), )
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-time_create', 'status', 'review')

    def __str__(self):
        return 'Наличный ' + super().__str__()


#Модель направления
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
    
    display_name = models.CharField('Отображение в админ панели',
                                    max_length=40,
                                    blank=True,
                                    null=True,
                                    default=None)
    actual_course = models.FloatField('Актуальный курс обмена',
                                      blank=True,
                                      null=True,
                                      default=None)
    
    def __str__(self):
        return self.display_name
    
    def clean(self) -> None:
        if self.valute_from.type_valute == self.valute_to.type_valute:
            raise ValidationError('Значения "Отдаём" и "Получаем" должны иметь разные типы валют')
        
        if not 'Наличные' in (self.valute_from.type_valute, self.valute_to.type_valute):
            raise ValidationError('Одно из значений "Отдаём" и "Получаем" должно иметь наличный тип валюты, другое - безналичный')


#Модель готового направления
class ExchangeDirection(BaseExchangeDirection):
    exchange = models.ForeignKey(Exchange,
                                 on_delete=models.CASCADE,
                                 verbose_name='Обменник',
                                 related_name='directions')
    direction = models.ForeignKey(Direction,
                                  verbose_name='Направление для обмена',
                                  on_delete=models.CASCADE,
                                  related_name='exchange_directions')
    # city = models.CharField('Город', max_length=100)
    city = models.ForeignKey(City,
                             verbose_name='Город',
                             on_delete=models.CASCADE,
                             related_name='cash_directions')
    fromfee = models.FloatField('Процент', blank=True, null=True)
    params = models.CharField('Параметры', max_length=100, blank=True, null=True)

    class Meta:
        # unique_together = (("exchange", "city", "valute_from", "valute_to"), )
        unique_together = (("exchange", "city", "direction"), )
        verbose_name = 'Готовое направление'
        verbose_name_plural = 'Готовые направления'
        ordering = ['-is_active',
                    'exchange',
                    'city',
                    'direction__valute_from',
                    'direction__valute_to']
        # indexes = [
        #     models.Index(fields=['city', 'valute_from', 'valute_to'])
        # ]

    def __str__(self):
        # return f'{self.city}: {self.valute_from} -> {self.valute_to}'
        return f'{self.city}: {self.direction}'


#Модель элемента чёрного списка
class BlackListElement(models.Model):
    # city = models.CharField('Город', max_length=100)
    city = models.ForeignKey(City,
                             verbose_name='Город',
                             on_delete=models.CASCADE,
                             related_name='black_list_cash_directions')
    # valute_from = models.CharField('Отдаём', max_length=10)
    # valute_to = models.CharField('Получаем', max_length=10)
    direction = models.ForeignKey(Direction,
                                  verbose_name='Направление для обмена',
                                  on_delete=models.CASCADE,
                                  related_name='black_list_directions')

    class Meta:
        verbose_name = 'Элемент чёрного списка'
        verbose_name_plural = 'Элементы чёрного списка'
        # unique_together = (("city",  "valute_from", "valute_to"), )
        unique_together = (("city",  "direction"), )
        ordering = ['city',
                    'direction__valute_from',
                    'direction__valute_to']
        # indexes = [
        #     models.Index(fields=['city', 'valute_from', 'valute_to'])
        # ]

    #для более красивого вывода в чёрном списке
    def __str__(self):
        # return f'({self.city}): {self.valute_from} -> {self.valute_to}\n\n'
        return f'({self.city}): {self.direction}\n\n'