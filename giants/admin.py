# encoding=utf-8

from django.conf import settings
from django.contrib import admin

from giants.models import Person



class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description', 'display_date', 'wikipedia_link')

    def short_description(self, obj):
        return u'%s...' % obj.description[:settings.SHORT_DESC_LENGTH] \
            if len(obj.description) > settings.SHORT_DESC_LENGTH else obj.description

    short_description.short_description = 'Description'

admin.site.register(Person, PersonAdmin)