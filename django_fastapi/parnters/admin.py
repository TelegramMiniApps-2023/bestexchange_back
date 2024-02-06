from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from general_models.admin import BaseCommentAdmin, BaseCommentStacked, BaseReviewAdmin, BaseReviewStacked

from parnters.utils.endpoints import get_in_count, get_out_count

from .models import Exchange, Direction, Review, Comment, CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'exchange')

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
         return super().get_queryset(request).select_related('exchange', 'user')


class DirectionStacked(admin.StackedInline):
    model = Direction
    extra = 0
    classes = ['collapse']
    
    fields = ('get_direction_name', 'cities', 'percent', 'fix_amount', 'in_count_field', 'out_count_field')
    readonly_fields = ('get_direction_name', 'percent', 'fix_amount', 'in_count_field', 'out_count_field')
    show_change_link = True
    list_select_related = ['cities', 'direction']
    filter_horizontal = ('cities', )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
         return super().get_queryset(request).select_related('exchange', 'direction')

    def has_add_permission(self, request, obj=None):
        return False

    def get_direction_name(self, obj):
         return obj.direction.display_name
    
    get_direction_name.short_description = 'Название направления'

    def in_count_field(self, obj):
        # actual_course = obj.direction.actual_course
        # if actual_course < 1:
        #     a_c = 1 / actual_course
        #     res = a_c + (a_c * obj.percent / 100) + obj.fix_amount
        # else:
        #     res = 1
        # return res
        return get_in_count(obj)
    
    in_count_field.short_description = 'Сколько отдаём'

    def out_count_field(self, obj):
        # actual_course = obj.direction.actual_course
        # if actual_course < 1:
        #     res = 1
        # else:
        #     res = actual_course + (actual_course * obj.percent / 100) + obj.fix_amount
        # return res
        return get_out_count(obj)
    
    out_count_field.short_description = 'Сколько получаем'


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('exchange', 'direction')
    filter_horizontal = ('cities', )
    fields = (
        'direction',
        'cities',
        'course',
        # 'final_amount',
        'percent',
        'fix_amount',
        'in_count_field',
        'out_count_field',
        )
    # readonly_fields = ('course', 'in_count_field', 'out_count_field')
    readonly_fields = ('course', 'in_count_field', 'out_count_field')

    class Media:
         js = ('parnters/js/test.js', )

    def course(self, obj=None):
        return 0
    
    course.short_description = 'Курс обмена'

    def in_count_field(self, obj=None):
        return 0
    
    in_count_field.short_description = 'Сколько отдаём'
    
    def out_count_field(self, obj=None):
        return 0
    
    out_count_field.short_description = 'Сколько получаем'

    def has_add_permission(self, request: HttpRequest) -> bool:
        if not request.user.is_superuser:
            account = CustomUser.objects\
                                .select_related('exchange', 'user')\
                                .filter(user=request.user).get()
            #   account = CustomUser.objects.get(user=request.user)
            if not account.exchange:
                return False
            return super().has_add_permission(request)
        return False

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
         if not request.user.is_superuser:
            account = CustomUser.objects\
                                .select_related('exchange', 'user')\
                                .filter(user=request.user).get()
            # account = CustomUser.objects.get(user=request.user)
            return super().get_queryset(request)\
                            .select_related('exchange', 'direction', 'exchange__account__user')\
                            .filter(exchange=account.exchange)
         return super().get_queryset(request).select_related('exchange__account__user')

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if not request.user.is_superuser:
            account = CustomUser.objects.get(user=request.user)
            # partner_exchange = account.exchange
            obj.exchange = account.exchange
            # selected_exchange = form.cleaned_data['exchange']
            # print(selected_exchange)
            # if not partner_exchange == selected_exchange:
                # pass
            # else:
            #     obj.exchange = account.exchange

                # raise ValidationError('qwerty')
            # obj.full_clean()
            super().save_model(request, obj, form, change)
                # obj.save()
        else:
            return super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(BaseCommentAdmin):
    
    def get_queryset(self, request):
        if not request.user.is_superuser:
                # account = CustomUser.objects.get(user=request.user)
                account = CustomUser.objects\
                                    .select_related('exchange', 'user')\
                                    .filter(user=request.user).get()
                if not account.exchange:
                    return super().get_queryset(request).filter(status='На ожидании')
                return super().get_queryset(request)\
                                .select_related('review')\
                                .filter(review__in=account.exchange.reviews.all())
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
        if not request.user.is_superuser:
                account = CustomUser.objects\
                                    .select_related('exchange', 'user')\
                                    .filter(user=request.user).get()
                # account = CustomUser.objects.get(user=request.user)
                if not account.exchange:
                    return super().get_queryset(request).filter(status='На ожидании')
                return super().get_queryset(request)\
                                .select_related('exchange')\
                                .filter(exchange=account.exchange)  
        return super().get_queryset(request)


#Отображение отзывов на странице связанного обменника
class ReviewStacked(BaseReviewStacked):
    model = Review

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).select_related('exchange', 'exchange__account')


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('name', 'en_name', 'account')
    readonly_fields = ('is_active', )
    filter_horizontal = ()
    inlines = [DirectionStacked, ReviewStacked]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        if not request.user.is_superuser:
                # account = CustomUser.objects.get(user=request.user)
                account = CustomUser.objects\
                                    .select_related('exchange', 'user')\
                                    .filter(user=request.user).get()
                exchange = account.exchange
                if not exchange:
                    # вернуть пустой queryset
                    return super().get_queryset(request).filter(name='Не выбрано!!!')
                return super().get_queryset(request)\
                                .select_related('account', 'account__user', 'account__exchange')\
                                .filter(name=exchange.name)
        return super().get_queryset(request).select_related('account', 'account__user')
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        if not request.user.is_superuser:
            account = CustomUser.objects\
                                .select_related('exchange', 'user')\
                                .filter(user=request.user).get()
            # account = CustomUser.objects.get(user=request.user)
            if account.exchange:
                return False
        return super().has_add_permission(request)
    
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if not request.user.is_superuser and not change:
            account = CustomUser.objects\
                    .select_related('exchange', 'user')\
                    .filter(user=request.user).get()
            # account = CustomUser.objects.get(user=request.user)
            account.exchange = obj
            super().save_model(request, obj, form, change)
            account.save()
        else:
            return super().save_model(request, obj, form, change)
