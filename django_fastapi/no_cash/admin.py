from django.contrib import admin

from no_cash.models import Exchange, Direction, ExchangeDirection, Review, Comment
from no_cash.periodic_tasks import (manage_periodic_task_for_create,
                                    manage_periodic_task_for_update,
                                    manage_periodic_task_for_parse_black_list)

from general_models.admin import (BaseCommentAdmin,
                                  BaseCommentStacked,
                                  BaseReviewAdmin,
                                  BaseReviewStacked,
                                  BaseExchangeAdmin,
                                  BaseExchangeDirectionAdmin,
                                  BaseExchangeDirectionStacked,
                                  BaseDirectionAdmin)
from general_models.tasks import parse_reviews_for_exchange


#Отображение комментариев в админ панели
@admin.register(Comment)
class CommentAdmin(BaseCommentAdmin):
    pass


#Отображение комментариев на странице связанного отзыва
class CommentStacked(BaseCommentStacked):
    model = Comment


#Отображение отзывов в админ панели
@admin.register(Review)
class ReviewAdmin(BaseReviewAdmin):
    inlines = [CommentStacked]


#Отображение отзывов на странице связанного обменника
class ReviewStacked(BaseReviewStacked):
    model = Review

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('exchange')


#Отображение готовых направлений на странице связанного обменника
class ExchangeDirectionStacked(BaseExchangeDirectionStacked):
    model = ExchangeDirection

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('exchange')


#Отображение обменников в админ панели
@admin.register(Exchange)
class ExchangeAdmin(BaseExchangeAdmin):
    inlines = [ExchangeDirectionStacked, ReviewStacked]

    def save_model(self, request, obj, form, change):
        update_fields = []

        if change:
            print('CHANGE!!!')
            for key, value in form.cleaned_data.items():
                # print(obj.name)
                # print('key', key)
                # print('value', value)
                if value != form.initial[key]:
                    match key:
                        case 'period_for_create':
                            manage_periodic_task_for_create(obj.pk,
                                                            obj.name,
                                                            value)
                        case 'period_for_update':
                            manage_periodic_task_for_update(obj.pk,
                                                            obj.name,
                                                            value)
                        case 'period_for_parse_black_list':
                            manage_periodic_task_for_parse_black_list(obj.pk,
                                                                      obj.name,
                                                                      value)
                    update_fields.append(key)
            obj.save(update_fields=update_fields)
        else:
            print('NOT CHANGE!!!!')
            super().save_model(request, obj, form, change)
            parse_reviews_for_exchange.delay(obj.en_name, 'no_cash')


#Отображение направлений в админ панели
@admin.register(Direction)
class DirectionAdmin(BaseDirectionAdmin):
    pass


#Отображение готовых направлений в админ панели
@admin.register(ExchangeDirection)
class ExchangeDirectionAdmin(BaseExchangeDirectionAdmin):
    def get_display_name(self, obj):
        # return f'{obj.exchange} ({obj.valute_from} -> {obj.valute_to})'
        return f'{obj.exchange} ({obj.direction})'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('exchange',
                                                            'direction',
                                                            'direction__valute_to',
                                                            'direction__valute_from')