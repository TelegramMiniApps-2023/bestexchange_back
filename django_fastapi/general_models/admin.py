from typing import Any

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe
from django.http.request import HttpRequest

from django_celery_beat.models import (SolarSchedule,
                                       PeriodicTask,
                                       IntervalSchedule,
                                       ClockedSchedule,
                                       CrontabSchedule)

from .utils.admin import ReviewAdminMixin
from .utils.endpoints import try_generate_icon_url
from .models import Valute


#DONT SHOW PERIODIC TASKS IN ADMIN PANEL
admin.site.unregister(SolarSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(CrontabSchedule)

#DONT SHOW USER AND GROUP IN ADMIN PANEL
admin.site.unregister(User)
admin.site.unregister(Group)


#Отображение валют в админ панели
@admin.register(Valute)
class ValuteAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'get_icon', 'type_valute')
    fields = ('name', 'code_name', 'icon_url', 'get_icon', 'type_valute')
    readonly_fields = ('get_icon', )
    search_fields = ('name', )

    def get_icon(self, obj):
        if obj.icon_url:
            icon_url = try_generate_icon_url(obj)
            return mark_safe(f"<img src='{icon_url}' width=40")

    get_icon.short_description = 'Текущая иконка'


#Базовое отображение комментариев в админ панели
class BaseCommentAdmin(ReviewAdminMixin, admin.ModelAdmin):
    list_display = ("username", "time_create", "moderation")
    readonly_fields = ('moderation', 'review')
    ordering = ('-time_create', 'moderation')

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    

#Базовое отображение комментариев на странице связанного отзыва
class BaseCommentStacked(admin.StackedInline):
    extra = 0
    readonly_fields = ('moderation', )
    ordering = ('-time_create', 'status')


#Базовое отображение отзывов в админ панели
class BaseReviewAdmin(ReviewAdminMixin, admin.ModelAdmin):
    list_display = ("username", "exchange", "time_create", "comment_count", "moderation")
    readonly_fields = ('moderation', )
    ordering = ('-time_create', 'status')
    
    def comment_count(self, obj):
        return obj.comments.count()
    
    comment_count.short_description = 'Число комментариев'


#Базовое отображение отзывов на странице связанного обменника
class BaseReviewStacked(admin.StackedInline):
    extra = 0
    readonly_fields = ('moderation', )
    show_change_link = True


#Базовое отображение готовых направлений в админ панели
class BaseExchangeDirectionAdmin(admin.ModelAdmin):
    list_display = ("get_display_name", )

    def has_change_permission(self, request, obj = None):
        return False
    
    def has_add_permission(self, request, obj = None):
        return False


#Базовое отображение готовых направлений на странице связанного обменника
class BaseExchangeDirectionStacked(admin.StackedInline):
    
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
                "fields": ["name", "xml_url", "partner_link", "is_active", ("period_for_create", "period_for_update", "period_for_parse_black_list")],
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

    def get_direction_name(self, obj):
        return f'{obj.valute_from} -> {obj.valute_to}'
    
    def has_change_permission(self, request, obj = None):
        return False