# coding=utf-8

import datetime
import time

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify


from models import Person


def home(request):
    """
    Just redirects to the person of the current day
    """
    month = time.strftime("%m")
    day = time.strftime("%d")
    person = Person.objects.get(display_month=month, display_day=day)

    return redirect(person.get_url())


def person(request, template_name='person.html', month=None, day=None, name=None):
    """
    Displays one person.
    """
    person_of_today = get_object_or_404(Person, display_month=month, display_day=day)

    # redirect to correct url in case there is no or the wrong slug of the person
    if not name or name and name != slugify(person_of_today.name):
        return redirect(person_of_today.get_url(), permanent=True)

    date_string = u'%s-%s-%s' % (time.strftime("%Y"), month, day)
    current_date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()

    context = {
        'person': person_of_today,
        'current_date': current_date,
    }

    return render(request, template_name, context)
