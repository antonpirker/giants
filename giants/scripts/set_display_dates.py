# encoding=utf-8

import datetime
import random
import sys

from giants.models import Person


def run():
    """
    Sets display dates of the persons in a random order
    """
    sys.stdout.write('Setting display dates\n')

    count = Person.objects.all().count()
    max_id = Person.objects.all().order_by('-pk')[0].pk + 1

    start_date = datetime.datetime.now()

    ids = range(0, max_id)
    random.shuffle(ids)

    for idx, pk in enumerate(ids):
        try:
            person = Person.objects.get(pk=pk)
            current_date = start_date + datetime.timedelta(days=idx)

            person.display_month = current_date.month
            person.display_day = current_date.day
            person.save()

        except Person.DoesNotExist:
            pass

        sys.stdout.write(u'\rProcessing %s/%s ...' % (idx, count))
        sys.stdout.flush()

    sys.stdout.write('\nDone!\n')
    sys.stdout.flush()
