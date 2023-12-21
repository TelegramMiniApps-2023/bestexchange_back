from django.contrib import admin

from .periodic_tasks import (manage_periodic_task_for_create,
                             manage_periodic_task_for_update,
                             manage_periodic_task_for_parse_black_list)

from general_models.utils.admin import ReviewAdminMixin
from general_models.admin import (BaseCommentAdmin,
                                  BaseCommentStacked,
                                  BaseReviewAdmin,
                                  BaseReviewStacked,
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


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'country', 'is_parse')
    list_editable = ('is_parse', )
    list_select_related = ('country', )
    ordering = ('-is_parse', 'name')
    search_fields = ('name', 'country__name')
    list_per_page = 20


class CityStacked(admin.StackedInline):
    model = City
    extra = 0
    fields = ('is_parse', )
    ordering = ('-is_parse', 'name')
    

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", )
    inlines = [CityStacked]


@admin.register(Comment)
class CommentAdmin(BaseCommentAdmin):
    pass


class CommentStacked(BaseCommentStacked):
    model = Comment


@admin.register(Review)
class ReviewAdmin(BaseReviewAdmin):
    inlines = [CommentStacked]


class ReviewStacked(BaseReviewStacked):
    model = Review


class ExchangeDirectionStacked(BaseExchangeDirectionStacked):
    model = ExchangeDirection


@admin.register(Exchange)
class ExchangeAdmin(ReviewAdminMixin, admin.ModelAdmin):
    list_display = ("name", 'is_active')
    readonly_fields = ('is_active', 'direction_black_list')
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
                            manage_periodic_task_for_create(obj.name, value)
                        case 'period_for_update':
                            manage_periodic_task_for_update(obj.name, value)
                        case 'period_for_parse_black_list':
                            manage_periodic_task_for_parse_black_list(obj.name, value)
                    update_fields.append(key)

            obj.save(update_fields=update_fields)
        else:
            print('NOT CHANGE!!!!')
            return super().save_model(request, obj, form, change)
    

@admin.register(Direction)
class DirectionAdmin(BaseDirectionAdmin):
    pass
    

@admin.register(ExchangeDirection)
class ExchangeDirectionAdmin(BaseExchangeDirectionAdmin):
    def get_display_name(self, obj):
        return f'{obj.exchange} ({obj.city}: {obj.valute_from} -> {obj.valute_to})'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('exchange')