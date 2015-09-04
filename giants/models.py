# encoding=utf-8

import datetime

import pytz

from django.db import models



class Person(models.Model):
    """
    This represents one of the giants.
    """
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=2000, null=True, blank=True)
    image = models.ImageField(upload_to='person_images', null=True, blank=True)

    wikipedia_link = models.CharField(max_length=1000, null=True, blank=True)
    additional_link = models.CharField(max_length=1000, null=True, blank=True)

    display_date = models.DateField(null=True, blank=True)

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
