from collections.abc import Callable, Sequence
from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from general_models.admin import (BaseCommentAdmin,
                                  BaseCommentStacked,
                                  BaseReviewAdmin,
                                  BaseReviewStacked)
from general_models.utils.admin import ReviewAdminMixin

from partners.utils.endpoints import get_in_count, get_out_count, get_course_count

from .models import Exchange, Direction, Review, Comment, CustomUser, PartnerCity
from .utils.admin import (get_or_set_user_account_cache,
                          set_user_account_cache,
                          make_city_active)


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'exchange')

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
         return super().get_queryset(request).select_related('exchange', 'user')


class DirectionStacked(admin.StackedInline):
    model = Direction
    extra = 0
    show_change_link = True
    classes = ['collapse']
    
    fields = (
        'get_direction_name',
        # 'city',
        'percent',
        'fix_amount',
        'in_count_field',
        'out_count_field',
        )
    readonly_fields = (
        'get_direction_name',
        'percent',
        'fix_amount',
        'in_count_field',
        'out_count_field',
        )
    # list_select_related = ('city', 'direction')
    list_select_related = ('direction', )

    # filter_horizontal = ('cities', )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
         return super().get_queryset(request)\
                        .select_related('direction')

    def has_add_permission(self, request, obj=None):
        return False

    def get_direction_name(self, obj):
         return obj.direction.display_name
    
    get_direction_name.short_description = 'Название направления'

    def in_count_field(self, obj):
        return get_in_count(obj)
    
    in_count_field.short_description = 'Сколько отдаём'

    def out_count_field(self, obj):
        return get_out_count(obj)
    
    out_count_field.short_description = 'Сколько получаем'


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('direction', 'city', 'exchange_name')
    readonly_fields = (
        'course',
        'in_count_field',
        'out_count_field',
        )
    fields = (
        'city',
        'direction',
        'course',
        'percent',
        'fix_amount',
        'in_count_field',
        'out_count_field',
        )
    
    class Media:
         js = ('parnters/js/test.js', )
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if not request.user.is_superuser:
            if db_field.name == 'city':
                account = get_or_set_user_account_cache(request.user)
                field.queryset = field.queryset.filter(exchange=account.exchange)
        return field

    def exchange_name(self, obj=None):
        return obj.city.exchange

    def course(self, obj=None):
        # return 0
        return get_course_count(obj)
    
    course.short_description = 'Курс обмена'

    def in_count_field(self, obj=None):
        # return 0
        return get_in_count(obj)
    
    in_count_field.short_description = 'Сколько отдаём'
    
    def out_count_field(self, obj=None):
        # return 0
        return get_out_count(obj)
        
    out_count_field.short_description = 'Сколько получаем'

    def has_add_permission(self, request: HttpRequest) -> bool:
        if not request.user.is_superuser:
            account = get_or_set_user_account_cache(request.user)

            if account.exchange:
                return super().has_add_permission(request)
        
        return False
    
    def has_change_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        if request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            account = get_or_set_user_account_cache(request.user)
            queryset = queryset.select_related('city', 'direction')\
                                .filter(city__exchange=account.exchange)
        return queryset
    

class PartnerCityStacked(admin.StackedInline):
    model = PartnerCity
    extra = 0
    show_change_link = True
    classes = ['collapse']
    
    fields = (
        'get_city_name',
        # 'city',
        'has_office',
        'has_delivery',
        # 'in_count_field',
        # 'out_count_field',
        )
    readonly_fields = (
        'get_city_name',
        # 'percent',
        # 'fix_amount',
        # 'in_count_field',
        # 'out_count_field',
        )
    # list_select_related = ('city', 'direction')
    list_select_related = ('direction', )

    # filter_horizontal = ('cities', )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
         return super().get_queryset(request)\
                        .select_related('city')

    def get_city_name(self, obj=None):
        return obj.city
    
    get_city_name.short_description = 'Город'


@admin.register(PartnerCity)
class PartnerCityAdmin(admin.ModelAdmin):
    list_display = ('city', 'exchange')

    fields = (
        'city',
        ('has_office',
        'has_delivery',)
    )
    inlines = [DirectionStacked]

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if not change:
            if not request.user.is_superuser:
                account = get_or_set_user_account_cache(request.user)
                partner_cities = account.exchange.partner_cities\
                                                    .filter(city=obj.city)\
                                                    .all()
                ###
                make_city_active(obj.city)
                ###

                if partner_cities:
                    has_office = obj.has_office
                    has_delivery = obj.has_delivery
                    obj = partner_cities.get()
                    obj.has_office = has_office
                    obj.has_delivery = has_delivery
                    change = True
                else:
                    obj.exchange = account.exchange
        return super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        if not request.user.is_superuser:
            account = get_or_set_user_account_cache(request.user)
            if account.exchange:
                return super().has_add_permission(request)
        return False
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)\
                            .select_related('city',
                                            'exchange')
        if not request.user.is_superuser:
            account = get_or_set_user_account_cache(request.user)
            if account.exchange:
                queryset = queryset.filter(exchange=account.exchange)
            else:
                # вернуть пустой queryset
                queryset = queryset.filter(id=0)
        return queryset
    
    def get_city_name(self, obj=None):
        return obj.city
    
    get_city_name.short_description = 'Город'
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        path_info = request.environ['PATH_INFO']
        if path_info.endswith('change/'):
            readonly_fields = ('get_city_name', ) + readonly_fields
        return readonly_fields

    def get_fields(self, request: HttpRequest, obj: Any | None = ...) -> Sequence[Callable[..., Any] | str]:
        fields = super().get_fields(request, obj)
        path_info = request.environ['PATH_INFO']
        if path_info.endswith('change/'):
            fields = (
                'get_city_name',
                ('has_office', 'has_delivery')
            )
        return fields
    

# class DirectionStacked(admin.StackedInline):
#     model = Direction
#     extra = 0
#     show_change_link = True
#     classes = ['collapse']
    
#     fields = (
#         'get_direction_name',
#         # 'city',
#         'percent',
#         'fix_amount',
#         'in_count_field',
#         'out_count_field',
#         )
#     readonly_fields = (
#         'get_direction_name',
#         'percent',
#         'fix_amount',
#         'in_count_field',
#         'out_count_field',
#         )
#     # list_select_related = ('city', 'direction')
#     list_select_related = ('direction', )

#     # filter_horizontal = ('cities', )

#     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
#          return super().get_queryset(request)\
#                         .select_related('direction')

#     def has_add_permission(self, request, obj=None):
#         return False

#     def get_direction_name(self, obj):
#          return obj.direction.display_name
    
#     get_direction_name.short_description = 'Название направления'

#     def in_count_field(self, obj):
#         return get_in_count(obj)
    
#     in_count_field.short_description = 'Сколько отдаём'

#     def out_count_field(self, obj):
#         return get_out_count(obj)
    
#     out_count_field.short_description = 'Сколько получаем'


# @admin.register(Direction)
# class DirectionAdmin(admin.ModelAdmin):
#     # list_display = ('exchange', 'direction', 'cities')
#     list_display = ('direction', 'city', 'exchange_name')

#     # filter_horizontal = ('cities', )
#     # filter_vertical = ('cities', )
#     # search_fields = ('cities', )
#     # autocomplete_fields = ('cities', )
#     readonly_fields = (
#         'course',
#         'in_count_field',
#         'out_count_field',
#         )
#     fields = (
#         'city',
#         'direction',
#         # 'cities',
#         'course',
#         'percent',
#         'fix_amount',
#         'in_count_field',
#         'out_count_field',
#         )
    
#     class Media:
#          js = ('parnters/js/test.js', )
    
#     def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
#         field = super().formfield_for_foreignkey(db_field, request, **kwargs)
#         if db_field.name == 'city':
#             account = get_or_set_user_account_cache(request.user)
#             field.queryset = field.queryset.filter(exchange=account.exchange)
#         return field

#     def exchange_name(self, obj=None):
#         return obj.city.exchange

#     def course(self, obj=None):
#         return 0
    
#     course.short_description = 'Курс обмена'

#     def in_count_field(self, obj=None):
#         return 0
    
#     in_count_field.short_description = 'Сколько отдаём'
    
#     def out_count_field(self, obj=None):
#         return 0
    
#     out_count_field.short_description = 'Сколько получаем'

#     def has_add_permission(self, request: HttpRequest) -> bool:
#         if not request.user.is_superuser:
#             account = get_or_set_user_account_cache(request.user)

#             if account.exchange:
#                 return super().has_add_permission(request)
        
#         return False

#     def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
#         queryset = super().get_queryset(request)

#         if not request.user.is_superuser:
#             account = get_or_set_user_account_cache(request.user)
#             queryset = queryset.select_related('city', 'direction')\
#                                 .filter(city__exchange=account.exchange)
#         return queryset
        
        # if not request.user.is_superuser:
        #     account = get_or_set_user_account_cache(request.user)
        #     # queryset = queryset.select_related('exchange',
        #     #                                     'direction')\
        #     #                     .filter(exchange=account.exchange)
        #     queryset = queryset.select_related('direction')\
        #                         # .filter(exchange=account.exchange)

        # return queryset

    # def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
    #     if not request.user.is_superuser:
    #         account = get_or_set_user_account_cache(request.user)
    #         obj.exchange = account.exchange
    #         # super().save_model(request, obj, form, change)
    #     # else:
    #     #     return super().save_model(request, obj, form, change)
    #     return super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(BaseCommentAdmin):
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        if not request.user.is_superuser:
                account = get_or_set_user_account_cache(request.user)
                if account.exchange:
                    queryset = queryset\
                                    .select_related('review')\
                                    .filter(review__in=account.exchange.reviews.all())
                else:
                    queryset = queryset.filter(status='На ожидании')
        return queryset


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
        queryset = super().get_queryset(request)
        
        if not request.user.is_superuser:
                account = get_or_set_user_account_cache(request.user)
                if account.exchange:
                    queryset = queryset.select_related('exchange')\
                                        .filter(exchange=account.exchange)
                else:
                    queryset = queryset.filter(status='На ожидании')
        return queryset


#Отображение отзывов на странице связанного обменника
class ReviewStacked(BaseReviewStacked):
    model = Review

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request)\
                        .select_related('exchange',
                                        'exchange__account')


@admin.register(Exchange)
class ExchangeAdmin(ReviewAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'en_name', 'account')
    readonly_fields = ('is_active', )
    filter_horizontal = ()
    # inlines = [DirectionStacked, ReviewStacked]
    inlines = [PartnerCityStacked, ReviewStacked]


    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            readonly_fields = ('partner_link', ) + readonly_fields
        return readonly_fields


    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        if not request.user.is_superuser:
                account = get_or_set_user_account_cache(request.user)
                exchange = account.exchange
                
                if not exchange:
                    # вернуть пустой queryset
                    return super().get_queryset(request)\
                                    .filter(name='Не выбрано!!!')
                # вернуть обменник партнёра
                return super().get_queryset(request)\
                                .select_related('account',
                                                'account__user',
                                                'account__exchange')\
                                .filter(name=exchange.name)
        # вернуть все партнёрские обменники
        return super().get_queryset(request)\
                        .select_related('account', 'account__user')
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        if not request.user.is_superuser:
            account = get_or_set_user_account_cache(request.user)

            if account.exchange:
                return False
        return super().has_add_permission(request)
    
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if not request.user.is_superuser and not change:
            account = get_or_set_user_account_cache(request.user)
            account.exchange = obj
            super().save_model(request, obj, form, change)
            account.save()
            set_user_account_cache(account)
        else:
            return super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.delete()
        if not request.user.is_superuser:
            set_user_account_cache(request.user.moderator_account)

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet[Any]) -> None:
        super().delete_queryset(request, queryset)
        if not request.user.is_superuser:
            set_user_account_cache(request.user.moderator_account)
