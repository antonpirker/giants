# encoding=utf-8

import datetime
import os

from easy_thumbnails.files import get_thumbnailer
from PIL import Image, ImageFont, ImageDraw
import pytz

from django.conf import settings
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
    image_attribution = models.CharField(max_length=2000, null=True, blank=True)
    is_image_from_wikipedia = models.BooleanField(default=False)

    wikipedia_link = models.CharField(max_length=1000, null=True, blank=True)
    additional_link = models.CharField(max_length=1000, null=True, blank=True)

    display_order = models.IntegerField(null=True, blank=True, db_index=True)

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
        url = reverse('person', kwargs={'display_order': self.display_order,
                                        'name': slugify(self.name)})

        return url

    def get_full_url(self):
        """
        Returns the full url (including protocol and domain) of a person
        """
        return u'%s%s' % (settings.SITE_URL, self.get_url())

    def get_sharing_image(self):
        """
        Returns the url to a image that should be used for social sharing.
        If the image does not exist it will be created.
        """
        sharing_path = os.path.join(settings.MEDIA_ROOT, 'person_images_sharing')
        sharing_image_path = os.path.join(sharing_path, '%s.jpg' % slugify(self.name))

        if not os.path.isfile(sharing_image_path):
            if not os.path.exists(sharing_path):
                os.makedirs(sharing_path)

            font_file = os.path.join(settings.STATIC_ROOT, 'fonts', 'Bevan.ttf')
            font = ImageFont.truetype(font_file, 37)
            font2 = ImageFont.truetype(font_file, 27)

            WIDTH = 1200
            HEIGHT = 630
            background = Image.new('RGB', (WIDTH, HEIGHT), '#FFF0A5')

            # create circle mask for person image
            mask = Image.new('RGBA', (400, 400), color=(255, 255, 255, 0))
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([(0, 0), (400, 400)], fill=(255, 255, 255, 255))

            # draw person image
            if self.image:
                person_file = get_thumbnailer(self.image).get_thumbnail(settings.THUMBNAIL_ALIASES['']['big_image']).file.name
                if not person_file:
                    # the person_file is empty on the first creation of the thumbnail.
                    # i know this is a ugly hack, but its just a stupid side project website and therefore ok.
                    person_file = get_thumbnailer(self.image).get_thumbnail(settings.THUMBNAIL_ALIASES['']['big_image']).file.name

            else:
                person_file = os.path.join(settings.BASE_DIR, 'static', 'img', 'noimage.png')

            person_img = Image.open(person_file)
            img_w, img_h = person_img.size
            background.paste(person_img, ((WIDTH-img_w)/2, (HEIGHT-img_h)/2), mask)

            # draw person name
            draw = ImageDraw.Draw(background)
            w, h = draw.textsize(self.name.upper(), font=font)
            draw.text(((WIDTH-w)/2, 30), self.name.upper(), font=font, fill='#8E2800')

            # draw rectangle for 'logo'
            w, h = draw.textsize(settings.SITE_NAME, font=font2)
            draw.rectangle([((WIDTH-w)/2-50, HEIGHT-h-20), ((WIDTH-w)/2+w+50, HEIGHT)], fill='#8E2800')

            # draw giants of IT 'logo'
            draw.text((((WIDTH-w)/2), HEIGHT-h-15), settings.SITE_NAME, font=font2, fill='#FFF0A5')

            background.save(sharing_image_path)

        sharing_image_url = os.path.join(settings.MEDIA_URL,'person_images_sharing/', '%s.jpg' % slugify(self.name))

        return sharing_image_url
