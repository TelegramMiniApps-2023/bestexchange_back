from typing import Any

from django.db.models import Count
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.http.request import HttpRequest

from django_celery_beat.models import (SolarSchedule,
                                       PeriodicTask,
                                       IntervalSchedule,
                                       ClockedSchedule,
                                       CrontabSchedule)

from partners.utils.periodic_tasks import edit_time_for_task_check_directions_on_active

from .utils.admin import ReviewAdminMixin
from .utils.endpoints import try_generate_icon_url
from .models import Valute, PartnerTimeUpdate


#DONT SHOW PERIODIC TASKS IN ADMIN PANEL
admin.site.unregister(SolarSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(CrontabSchedule)

#DONT SHOW USER AND GROUP IN ADMIN PANEL
# admin.site.unregister(User)
# admin.site.unregister(Group)


@admin.register(PartnerTimeUpdate)
class PartnerTimeUpdateAdmin(admin.ModelAdmin):
    list_display = ('name', )
    # readonly_fields = ('name', )
    fields = (
        # 'name',
        'amount',
        'unit_time',
    )

    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        update_fields = []
        fields_to_update_task = {}

        if change:
            for key, value in form.cleaned_data.items():
                if value != form.initial[key]:
                    update_fields.append(key)
                match key:
                    case 'amount':
                        fields_to_update_task[key] = value
                    case 'unit_time':
                        fields_to_update_task[key] = value

            obj.save(update_fields=update_fields)

            match obj.name:
                case 'Управление временем проверки активности направлений':
                    task = 'check_update_time_for_directions_task'
                    edit_time_for_task_check_directions_on_active(task,
                                                                  fields_to_update_task)
                case 'Управление временем обнуления популярности направления':
                    task = 'update_popular_count_direction_time_task'
                    edit_time_for_task_check_directions_on_active(task,
                                                                  fields_to_update_task)
                # case 'Управление временем жизни направлений':
                #     edit_time_live_for_partner_directions(fields_to_update_task)
        else:
            return super().save_model(request, obj, form, change)


#Отображение валют в админ панели
@admin.register(Valute)
class ValuteAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'get_icon', 'type_valute')
    fields = ('name', 'en_name', 'code_name', 'icon_url', 'get_icon', 'type_valute')
    readonly_fields = ('get_icon', )
    search_fields = ('name', 'code_name', 'en_name')

    def get_icon(self, obj):
        if obj.icon_url:
            icon_url = try_generate_icon_url(obj)
            return mark_safe(f"<img src='{icon_url}' width=40")

    get_icon.short_description = 'Текущая иконка'


#Базовое отображение комментариев в админ панели
class BaseCommentAdmin(ReviewAdminMixin, admin.ModelAdmin):
    list_display = ("username", "get_exchange", "time_create", "moderation")
    readonly_fields = ('moderation', 'review')
    ordering = ('-time_create', 'moderation')
    list_filter = ('time_create', )

    def get_exchange(self, obj):
        return obj.review.exchange
    
    get_exchange.short_description = 'Обменник'

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def get_queryset(self, request):
        return super().get_queryset(request)\
                        .select_related('review', 'review__exchange')
    

#Базовое отображение комментариев на странице связанного отзыва
class BaseCommentStacked(admin.StackedInline):
    extra = 0
    readonly_fields = ('moderation', )
    ordering = ('-time_create', 'status')
    classes = ['collapse']

    def get_queryset(self, request):
        return super().get_queryset(request)\
                        .select_related('review', 'review__exchange')


#Базовое отображение отзывов в админ панели
class BaseReviewAdmin(ReviewAdminMixin, admin.ModelAdmin):
    list_display = ("username", "exchange", "time_create", "moderation", "comment_count")
    list_filter = ('time_create', )
    readonly_fields = ('moderation', )
    ordering = ('exchange__name', '-time_create', 'status')
    
    def comment_count(self, obj):
        return obj.comment_count
    
    comment_count.short_description = 'Число комментариев'

    def get_queryset(self, request):
        return super().get_queryset(request)\
                        .select_related('exchange')\
                        .annotate(comment_count=Count('comments'))


#Базовое отображение отзывов на странице связанного обменника
class BaseReviewStacked(admin.StackedInline):
    extra = 0
    readonly_fields = ('moderation', )
    show_change_link = True
    classes = ['collapse']


#Базовое отображение готовых направлений в админ панели
class BaseExchangeDirectionAdmin(admin.ModelAdmin):
    list_display = ("get_display_name", )

    def has_change_permission(self, request, obj = None):
        return False
    
    def has_add_permission(self, request, obj = None):
        return False
    
    def get_queryset(self, request):
        return super().get_queryset(request)\
                        .select_related('exchange')


#Базовое отображение готовых направлений на странице связанного обменника
class BaseExchangeDirectionStacked(admin.StackedInline):
    classes = ['collapse']
    
    def has_change_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False
    
    def has_add_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False


#Базовое отображение обменника в админ панели
class BaseExchangeAdmin(ReviewAdminMixin, admin.ModelAdmin):
    list_display = ("name", "xml_url", 'is_active')
    readonly_fields = ('direction_black_list', 'is_active')
    fieldsets = [
        (
            None,
            {
                "fields": [("name", "en_name"), "xml_url", "partner_link", "is_active", ("period_for_create", "period_for_update", "period_for_parse_black_list")],
            },
        ),
        (
            "Отсутствующие направления",
            {
                "classes": ["collapse"],
                "fields": ["direction_black_list"],
            },
        ),
    ]


#Базовое отображение направлений в админ панели
class BaseDirectionAdmin(admin.ModelAdmin):
    list_display = ('get_direction_name', )
    list_select_related = ('valute_from', 'valute_to')
    search_fields = ('valute_from__code_name', 'valute_to__code_name')
    readonly_fields = ('popular_count', )

    def get_direction_name(self, obj):
        return f'{obj.valute_from} -> {obj.valute_to}'
    
    get_direction_name.short_description = 'Название направления'
    
    def has_change_permission(self, request, obj = None):
        return False
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request)\
                        .select_related('valute_from',
                                        'valute_to')