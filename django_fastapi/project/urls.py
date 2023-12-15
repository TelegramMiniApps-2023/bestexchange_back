from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles import views

urlpatterns = [path("admin/", admin.site.urls)]


if settings.DEBUG:
    from django.urls import re_path

    urlpatterns += [re_path(r"^static/(?P<path>.*)$", views.serve)]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)