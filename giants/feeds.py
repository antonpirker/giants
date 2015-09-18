# encoding=utf-8

import datetime

from django.conf import settings
from django.contrib.syndication.views import Feed

from .models import Person


class PersonFeed(Feed):
    title = settings.SITE_NAME
    link = "/feed"
    description = 'We all stand on the shoulders of giants. Here are the giants of IT. One each day.'

    def items(self):
        import ipdb; ipdb.set_trace()
        time_online = datetime.datetime.now().date() - settings.SITE_START_DATE
        return Person.objects.filter(display_order__lte=time_online.days).order_by('-display_order')

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return item.get_full_url()