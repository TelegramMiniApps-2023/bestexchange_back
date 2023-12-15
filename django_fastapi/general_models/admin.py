from typing import Any

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe
from django.conf import settings
from django.http.request import HttpRequest

from django_celery_beat.models import (SolarSchedule,
                                       PeriodicTask,
                                       IntervalSchedule,
                                       ClockedSchedule,
                                       CrontabSchedule)
from .utils.admin import ReviewAdminMixin
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


@admin.register(Valute)
class ValuteAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'get_icon', 'type_valute')
    fields = ('name', 'code_name', 'icon_url', 'get_icon', 'type_valute')
    readonly_fields = ('get_icon', )
    search_fields = ('name', )

    def get_icon(self, obj):
        if obj.icon_url:
            return mark_safe(f"<img src='{settings.PROTOCOL}{settings.SITE_DOMAIN}{settings.DJANGO_PREFIX}{obj.icon_url.url}' width=40")
        
    get_icon.short_description = 'Текущая иконка'


class BaseCommentAdmin(ReviewAdminMixin, admin.ModelAdmin):
    list_display = ("username", "time_create", "moderation")
    readonly_fields = ('moderation', 'review')
    ordering = ('-time_create', 'moderation')

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    

class BaseCommentStacked(admin.StackedInline):
    extra = 0
    readonly_fields = ('moderation', )
    ordering = ('-time_create', 'status')


class BaseReviewAdmin(ReviewAdminMixin, admin.ModelAdmin):
    list_display = ("username", "exchange", "time_create", "comment_count", "moderation")
    readonly_fields = ('moderation', )
    ordering = ('-time_create', 'status')
    
    def comment_count(self, obj):
        return obj.comments.count()
    
    comment_count.short_description = 'Число комментариев'


class BaseReviewStacked(admin.StackedInline):
    extra = 0
    readonly_fields = ('moderation', )
    show_change_link = True


class BaseExchangeDirectionAdmin(admin.ModelAdmin):
    list_display = ("get_display_name", )

    def has_change_permission(self, request, obj = None):
        return False
    
    def has_add_permission(self, request, obj = None):
        return False


class BaseExchangeDirectionStacked(admin.StackedInline):
    
    def has_change_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False
    
    def has_add_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False
    

class BaseDirectionAdmin(admin.ModelAdmin):
    list_display = ('get_direction_name', )
    list_select_related = ('valute_from', 'valute_to')
    search_fields = ('valute_from__code_name', 'valute_to__code_name')

    def get_direction_name(self, obj):
        return f'{obj.valute_from} -> {obj.valute_to}'
    
    def has_change_permission(self, request, obj = None):
        return False