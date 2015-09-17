# encoding=utf-8

from django.conf import settings


def site(request):
    """
    Adds some useful information to the template context
    """
    context = {
        'SITE_URL': settings.SITE_URL,
        'SITE_NAME': settings.SITE_NAME,
    }

    return context