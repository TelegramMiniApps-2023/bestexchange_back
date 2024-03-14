from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles import views


admin.site.site_header = 'Админ сайт телеграм бота BestExChange'


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("admin/", admin.site.urls),
    path('sentry-debug/', trigger_error),
    path('summernote/', include('django_summernote.urls')),
    ]


if settings.DEBUG:
    from django.urls import re_path

    urlpatterns += [
    path("__debug__/", include("debug_toolbar.urls")),
    ]

    urlpatterns += [re_path(r"^static/(?P<path>.*)$", views.serve)]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)