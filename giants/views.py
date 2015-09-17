# coding=utf-8

import datetime
import time

from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect


from models import Person


def home(request):
    """
    Just redirects to the person of the current day
    """
    month = time.strftime("%m")
    day = time.strftime("%d")
    giant_url = reverse('person', kwargs={'month': month, 'day': day})

    return redirect(giant_url)


def person(request, template_name='person.html', month=None, day=None):
    """
    Displays one person.
    """
    try:
        person_of_today = Person.objects.get(display_month=month, display_day=day)
    except Person.DoesNotExist:
        person_of_today = Person.objects.filter(display_month__isnull=True,
                                                display_day__isnull=True).order_by('?').first()

    date_string = u'%s-%s-%s' % (time.strftime("%Y"), month, day)
    current_date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()

    context = {
        'person': person_of_today,
        'current_date': current_date,
    }

    return render(request, template_name, context)
