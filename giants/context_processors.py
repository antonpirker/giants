# encoding=utf-8

from django.conf import settings


def site(request):
    return {'SITE_URL': settings.SITE_URL}