# encoding=utf-8

from django.conf import settings
from django.contrib import admin

from easy_thumbnails.files import get_thumbnailer

from giants.models import Person



class PersonAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'name', 'short_description', 'display_date', 'clickable_wikipedia_link')

    def short_description(self, obj):
        return u'%s...' % obj.description[:settings.SHORT_DESC_LENGTH] \
            if len(obj.description) > settings.SHORT_DESC_LENGTH else obj.description

    short_description.short_description = 'Description'


    def clickable_wikipedia_link(self, obj):
        return u'<a href="%s">%s</a>' % (obj.wikipedia_link, obj.wikipedia_link)

    clickable_wikipedia_link.allow_tags = True
    clickable_wikipedia_link.short_description = 'Wikipedia Link'


    def thumbnail(self, obj):
        if obj.image:
            thumb_url = get_thumbnailer(obj.image)['admin_thumbnail'].url
            return '<img src="%s" />' % thumb_url
        else:
            return ''

    thumbnail.allow_tags = True
    thumbnail.short_description = 'Image'

admin.site.register(Person, PersonAdmin)