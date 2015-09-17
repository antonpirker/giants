# coding=utf-8

import datetime
import time

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.http import HttpResponseForbidden
from django.template import RequestContext


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

    date_string = u'%s-%s-%s' % (time.strftime("%Y"), month, day)
    current_date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    today = datetime.datetime.now().date()

    # do not allow to look into the future
    if current_date > today:
        # i do not know, why I need to do this by hand,
        # but it does not work like described in the documentation
        # https://docs.djangoproject.com/en/1.4/topics/http/views/#the-403-http-forbidden-view
        from django.template.loader import get_template
        template = get_template('403.html')
        html = template.render()
        return HttpResponseForbidden(html)

    # redirect to correct url in case there is no or the wrong slug of the person
    if not name or name and name != slugify(person_of_today.name):
        return redirect(person_of_today.get_url(), permanent=True)

    try:
        yesterday = current_date - datetime.timedelta(days=1)
        person_of_yesterday = Person.objects.get(display_month=yesterday.month, display_day=yesterday.day)

    except Person.DoesNotExist:
        person_of_yesterday = None

    try:
        tomorrow = current_date + datetime.timedelta(days=1)
        if tomorrow > today:
            # no links into the future
            person_of_tomorrow = None
        else:
            person_of_tomorrow = Person.objects.get(display_month=tomorrow.month, display_day=tomorrow.day)

    except Person.DoesNotExist:
        person_of_tomorrow = None

    context = RequestContext(request)
    context.push({
        'person': person_of_today,
        'current_date': current_date,
        'link_prev': person_of_yesterday.get_url() if person_of_yesterday else None,
        'link_next': person_of_tomorrow.get_url() if person_of_tomorrow else None,
    })

    return render(request, template_name, context)
