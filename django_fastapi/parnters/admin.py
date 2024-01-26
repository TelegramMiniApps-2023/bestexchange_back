from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from cash.models import CustomUser

# from django_dynamic_admin_forms.admin import DynamicModelAdminMixin

from general_models.admin import BaseCommentAdmin, BaseCommentStacked, BaseReviewAdmin, BaseReviewStacked

from .models import Exchange, Direction, Review, Comment

class DirectionStacked(admin.StackedInline):
    model = Direction
    extra = 0
    fields = ('direction', 'cities', 'course', 'percent', 'fix_amount')
    # dynamic_fields = ('fix_amount',)
    readonly_fields = ('course', )
    # ordering = ('-is_parse', 'name')
    show_change_link = True
    list_select_related = ['cities', 'direction']
    filter_horizontal = ('cities', )
    # prepopulated_fields = {'fix_amount' : ('percent',)}

    # def get_dinamic_percent_field(self, data):
    #      print('hi')
    #      return data.get('fix_amount')

    def course(self, obj=None):
        return 94.35

    # def final_amount(self, obj):
    #     return self.course(obj) + obj.percent * self.course(obj)

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('exchange', 'direction')
    filter_horizontal = ('cities', )
    fields = ('exchange', 'direction', 'cities', 'course', 'percent', 'fix_amount')
    readonly_fields = ('course', )
    # dynamic_fields = ('exchange',)

    def course(self, obj=None):
        return None
    
    class Media:
         js = ('parnters/js/test.js', )
    
    # def get_dynamic_exchange_field(self, data):
    #      print('hi')
    #     #  data['22'] = 22
    #      queryset = Exchange.objects.all()
    #      if self.course() == 94.35:     
    #         queryset = Exchange.objects.filter(name__icontains='test')
    #      value = data.get('exchange')
    #      hidden = False
    #      return queryset, value, hidden


@admin.register(Comment)
class CommentAdmin(BaseCommentAdmin):
    
    def get_queryset(self, request):
        if not request.user.is_superuser:
                account = CustomUser.objects.get(user=request.user)
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
                account = CustomUser.objects.get(user=request.user)
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
        return super().get_queryset(request).select_related('exchange')


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('name', 'en_name')
    readonly_fields = ('is_active', )
    filter_horizontal = ()
    inlines = [DirectionStacked, ReviewStacked]
