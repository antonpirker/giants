# encoding=utf-8

import re
import requests
import sys

from lxml import html

from giants.models import Person

from django.core.files.base import ContentFile



def run():
    """
    Fetches an image of each giant from Wikipedia
    """
    sys.stdout.write('Importing images of giants from Wikipedia\n')

    WIKI_LINK = 'https://en.wikipedia.org/w/api.php?action=query&titles=%s&prop=revisions&rvprop=content&format=json'
    COMMONS_LINK = 'https://tools.wmflabs.org/magnus-toolserver/commonsapi.php?image=%s'

    count = Person.objects.all().count()
    max_id = Person.objects.all().order_by('-pk')[0].pk

    for idx in range(0, max_id):
        try:
            person = Person.objects.get(pk=idx)
            person_name = person.wikipedia_link.split('/')[-1]

            try:
                page = requests.get(WIKI_LINK % person_name)

                try:
                    image_name = re.search('image([^\=]*)([=]+)([^\|]*)', page.text.replace('\\n', '')).group(3).lstrip().rstrip()
                except AttributeError:
                    image_name = re.search('File([^\:]*)([:]+)([^\|]*)', page.text.replace('\\n', '')).group(3).lstrip().rstrip()

                page = requests.get(COMMONS_LINK % image_name)
                tree = html.fromstring(page.text.replace('encoding', 'bla'))  # because lxml does not like it if there is a encoding definition
                image_url = tree.xpath('//urls/file')[0].text

                page = requests.get(image_url)
                person.image.save(image_name, ContentFile(page.content))
                person.is_image_from_wikipedia = True
                person.save()
            except (AttributeError, IndexError):
                pass

        except Person.DoesNotExist:
            pass

        sys.stdout.write(u'\rProcessing %s/%s ...' % (idx, count))
        sys.stdout.flush()

    sys.stdout.write('\nDone!\n')
    sys.stdout.flush()
