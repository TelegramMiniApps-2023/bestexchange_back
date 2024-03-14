from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from general_models.models import BaseExchange, BaseReview, BaseComment

from cash.models import Direction as CashDirection, City

from .utils.models import get_limit_direction, is_positive_validator


class Exchange(BaseExchange):
    
    class Meta:
        verbose_name = 'Обменник'
        verbose_name_plural = 'Обменники'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['en_name']),
        ]


class CustomUser(models.Model):
    limit_user = Q(is_superuser=False)

    user = models.OneToOneField(User,
                                verbose_name='Пользователь',
                                on_delete=models.CASCADE,
                                limit_choices_to=limit_user,
                                related_name='moderator_account')
    exchange = models.OneToOneField(Exchange,
                                    verbose_name='Партнёрский обменник',
                                    unique=True,
                                    blank=True,
                                    null=True,
                                    default=None,
                                    on_delete=models.SET_DEFAULT,
                                    related_name='account')
    
    class Meta:
        verbose_name = 'Администратор обменника'
        verbose_name_plural = 'Администраторы обменников'

    def __str__(self):
        return f'Пользователь: {self.user}, Обменник: {self.exchange}'


class PartnerCity(models.Model):
    exchange = models.ForeignKey(Exchange,
                                 on_delete=models.CASCADE,
                                 related_name='partner_cities')
    city = models.ForeignKey(City,
                             on_delete=models.CASCADE,
                             verbose_name='Город',
                             related_name='partner_cities')
    has_delivery = models.BooleanField('Есть ли доставка?', default=False)
    has_office = models.BooleanField('Есть ли офис?', default=False)

    class Meta:
        verbose_name = 'Партнёрский город'
        verbose_name_plural = 'Партнёрские города'
        ordering = ('exchange', 'city')

    def __str__(self):
        return f'{self.city}'


class Direction(models.Model):
    limit_direction = get_limit_direction()

    city = models.ForeignKey(PartnerCity,
                             on_delete=models.CASCADE,
                             verbose_name='Город',
                             related_name='partner_directions')
    direction = models.ForeignKey(CashDirection,
                                  verbose_name='Направление',
                                  on_delete=models.CASCADE,
                                  limit_choices_to=limit_direction,
                                  related_name='partner_directions')

    percent = models.FloatField('Процент',
                                default=0,
                                validators=[is_positive_validator])
    fix_amount = models.FloatField('Фиксированная ставка',
                                   default=0,
                                   validators=[is_positive_validator])
    time_update = models.DateTimeField('Последнее обновление',
                                       auto_now_add=True,
                                       help_text='Время указано по московскому часовому поясу. При не обновлении процентов или фикс. ставки в течении 3 дней, направление становится неактивным.')
    is_active = models.BooleanField('Активно?', default=True)

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'
        unique_together = (('city', 'direction'), )
        ordering = ('city__exchange', 'city', 'direction')

    def __str__(self):
        return f'{self.city} - {self.direction}'


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