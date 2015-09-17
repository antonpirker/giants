# encoding=utf-8

import datetime

import pytz

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify



class Person(models.Model):
    """
    This represents one of the giants.
    """
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=2000, null=True, blank=True)
    image = models.ImageField(upload_to='person_images', null=True, blank=True)

    wikipedia_link = models.CharField(max_length=1000, null=True, blank=True)
    additional_link = models.CharField(max_length=1000, null=True, blank=True)

    display_month = models.IntegerField(null=True, blank=True, db_index=True)
    display_day = models.IntegerField(null=True, blank=True, db_index=True)

    created = models.DateTimeField(editable=False, null=False, blank=False)
    modified = models.DateTimeField(editable=False, null=False, blank=False)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.pk)

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        if not self.pk:
            self.created = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        else:
            if not self.created:
                self.created = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        self.modified = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        super(Person, self).save(*args, **kwargs)

    def get_url(self):
        """
        Returns the (long) URL of a person
        """
        url = reverse('person', kwargs={'month': '%02d' % self.display_month,
                                        'day': '%02d' % self.display_day,
                                        'name': slugify(self.name)})

        return url
