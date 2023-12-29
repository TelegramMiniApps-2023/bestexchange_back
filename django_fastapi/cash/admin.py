from django.contrib import admin
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


#Отображение готовых направлений на странице связанного обменника
class ExchangeDirectionStacked(BaseExchangeDirectionStacked):
    model = ExchangeDirection


#Отображение обменников в админ панели
@admin.register(Exchange)
class ExchangeAdmin(BaseExchangeAdmin):
    inlines = [ExchangeDirectionStacked, ReviewStacked]

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
            return super().save_model(request, obj, form, change)
    

#Отображение направлений в админ панели
@admin.register(Direction)
class DirectionAdmin(BaseDirectionAdmin):
    pass
    

#Отображение готовых направлений в админ панели
@admin.register(ExchangeDirection)
class ExchangeDirectionAdmin(BaseExchangeDirectionAdmin):
    def get_display_name(self, obj):
        return f'{obj.exchange} ({obj.city}: {obj.valute_from} -> {obj.valute_to})'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('exchange')