# encoding=utf-8

import datetime

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import Person


class PersonFeed(Feed):
    link = "/feed"
    feed_type = Atom1Feed
    title = settings.SITE_NAME
    subtitle = 'We all stand on the shoulders of giants. Here are the giants of IT. One each day.'

    def items(self):
        time_online = datetime.datetime.now().date() - settings.SITE_START_DATE
        return Person.objects.filter(display_order__lte=time_online.days).order_by('-display_order')

    def author_email(self, item):
        return 'anton@ignaz.at'

    def author_name(self, item):
        return 'Anton Pirker'

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        desc = '%(text)s\n\n<a href="%(link)s">%(link)s</a>' % {
            'text': item.description,
            'link': item.wikipedia_link
        }
        return desc

    def item_link(self, item):
        return item.get_full_url()

    def item_author_email(self, item):
        return 'anton@ignaz.at'

    def item_author_name(self, item):
        return 'Anton Pirker'
