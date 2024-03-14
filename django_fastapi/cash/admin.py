from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.safestring import mark_safe

from general_models.utils.endpoints import try_generate_icon_url

from .periodic_tasks import (manage_periodic_task_for_create,
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

from .models import (Country,
                     City,
                     Exchange,
                     Direction,
                     ExchangeDirection,
                     Review,
                     Comment)


#Отображение городов в админ панели
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'country', 'is_parse')
    list_editable = ('is_parse', )
    list_select_related = ('country', )
    ordering = ('-is_parse', 'name')
    search_fields = ('name', 'country__name')
    list_per_page = 20


#Отображение городов на странице связанной страны
class CityStacked(admin.StackedInline):
    model = City
    extra = 0
    fields = ('is_parse', )
    ordering = ('-is_parse', 'name')
    show_change_link = True


#Отображение стран в админ панели
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", 'get_icon')
    readonly_fields = ('get_icon', )
    search_fields = ('name', )
    inlines = [CityStacked]

    def get_icon(self, obj):
        if obj.icon_url:
            icon_url = try_generate_icon_url(obj)
            return mark_safe(f"<img src='{icon_url}' width=40")
    
    get_icon.short_description = 'Текущий флаг'


#Отображение комментариев в админ панели
@admin.register(Comment)
class CommentAdmin(BaseCommentAdmin):
    
    def get_queryset(self, request):
        return super().get_queryset(request)


#Отображение комментариев на странице связанного отзыва
class CommentStacked(BaseCommentStacked):
    model = Comment

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).select_related('review')


#Отображение отзывов в админ панели
@admin.register(Review)
class ReviewAdmin(BaseReviewAdmin):
    inlines = [CommentStacked]

    def has_add_permission(self, request: HttpRequest) -> bool:
        if not request.user.is_superuser:
                return False
        return super().has_add_permission(request)

    def get_queryset(self, request): 
        return super().get_queryset(request)


#Отображение отзывов на странице связанного обменника
class ReviewStacked(BaseReviewStacked):
    model = Review

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).select_related('exchange')


#Отображение готовых направлений на странице связанного обменника
class ExchangeDirectionStacked(BaseExchangeDirectionStacked):
    model = ExchangeDirection

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).select_related('exchange')


#Отображение обменников в админ панели
@admin.register(Exchange)
class ExchangeAdmin(BaseExchangeAdmin):
    inlines = [ExchangeDirectionStacked, ReviewStacked]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request)
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return super().has_add_permission(request)

    def save_model(self, request, obj, form, change):
        update_fields = []

        if change: 
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
            parse_reviews_for_exchange.delay(obj.en_name, 'cash')
    

#Отображение направлений в админ панели
@admin.register(Direction)
class DirectionAdmin(BaseDirectionAdmin):
    # readonly_fields = ('display_name', 'actual_course')

    def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> list[str] | tuple[Any, ...]:
        readonly_fileds = super().get_readonly_fields(request, obj)
        readonly_fileds += ('display_name', 'actual_course')
        return readonly_fileds

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).select_related('valute_from', 'valute_to')
    

#Отображение готовых направлений в админ панели
@admin.register(ExchangeDirection)
class ExchangeDirectionAdmin(BaseExchangeDirectionAdmin):
    def get_display_name(self, obj):
        # return f'{obj.exchange} ({obj.city}: {obj.valute_from} -> {obj.valute_to})'
        return f'{obj.exchange} ({obj.city}: {obj.direction})'


    def get_queryset(self, request):
        return super().get_queryset(request).select_related('exchange')