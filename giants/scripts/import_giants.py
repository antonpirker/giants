# encoding=utf-8

import json
import os
import sys

import gspread
from oauth2client.client import SignedJwtAssertionCredentials

from django.conf import settings

from giants.models import Person



def run():
    """
    Connects to Google Sheets and imports all the persons saved in a spreadsheet
    """
    sys.stdout.write('Importing giants from spreadsheet\n')

    key_file_name = os.path.abspath(os.path.join(settings.BASE_DIR, 'config', 'giants-3c4fa8ec2e7d.json'))

    json_key = json.load(open(key_file_name))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

    gc = gspread.authorize(credentials)

    worksheet = gc.open('Giants of IT - We stand on the shoulders of giants.').sheet1

    count = worksheet.row_count-1
    for idx in range(1, count):
        row = worksheet.row_values(idx)

        try:
            person, created = Person.objects.get_or_create(name=row[0])
            person.display_order = idx
            person.description = row[1]
            person.wikipedia_link = row[2]
            try:
                person.additional_link = row[3]
            except:
                pass

            person.save()

        except IndexError:  # catch empty rows
            pass

        sys.stdout.write(u'\rProcessing %s/%s ...' % (idx, count))
        sys.stdout.flush()

    sys.stdout.write('\nDone!\n')
    sys.stdout.flush()








