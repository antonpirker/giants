# encoding=utf-8

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from . import views
from .feeds import PersonFeed

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.home, name='home'),
    url(r'^(?P<display_order>[0-9]+)$', views.person, name='person-short-url'),
    url(r'^(?P<display_order>[0-9]+)/(?P<name>[\w-]+)$', views.person, name='person'),

    url(r'^feed$', PersonFeed()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)