from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

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


class Direction(models.Model):
    limit_direction = Q(valute_from__type_valute='Криптовалюта',
                       valute_to__type_valute='Наличные') | Q(valute_from__type_valute='Наличные',
                       valute_to__type_valute='Криптовалюта')

    exchange = models.ForeignKey(Exchange,
                                 verbose_name='Обменник',
                                 on_delete=models.CASCADE,
                                 related_name='directions',
                                 blank=True,
                                 null=True,
                                 default=None)
    direction = models.ForeignKey(CashDirection,
                                  verbose_name='Направление',
                                  on_delete=models.CASCADE,
                                  limit_choices_to=limit_direction,
                                  related_name='partner_directions')
    cities = models.ManyToManyField(City,
                                    verbose_name='Города')
    percent = models.FloatField('Процент',
                                blank=True,
                                null=True,
                                default=0)
    fix_amount = models.FloatField('Фиксированная ставка',
                                   blank=True,
                                   null=True,
                                   default=0)

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    def __str__(self):
        return f'{self.direction}'


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