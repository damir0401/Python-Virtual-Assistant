from __future__ import print_function
import datetime
import os.path
from voice_assistant import *

import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
DAY_EXT = ['st', 'nd', 'rd', 'th']
MONTHS = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8,
          'september': 9, 'october': 10, 'november': 11, 'december': 12}
WEEKDAYS = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
today = datetime.datetime.now()
local = pytz.timezone('Asia/Almaty')

def google_authentication():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


SERVICE = google_authentication()


def get_events(day, service):
    try:

        # Call the Calendar API
        time_min = datetime.datetime.combine(day, datetime.time.min).astimezone(local)
        time_max = datetime.datetime.combine(day, datetime.time.max).astimezone(local)
        print(f'Getting the upcoming events on {day}')
        speak(f'Getting the upcoming events on {day}')
        events_result = service.events().list(calendarId='primary', timeMin=time_min.isoformat(),
                                              timeMax=time_max.isoformat(), singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print(f'No upcoming events found on {day}')
            speak(f'No upcoming events found on {day}')
            return

        for event in events:
            start = event['start'].get('dateTime')
            end = event['end'].get('dateTime')
            date = start.split('T')[0]
            start_time_list = start.split('T')[1].split('+')[0].split(':')
            if int(start_time_list[0]) > 12:
                if int(start_time_list[1]) != 0:
                    start_time = str(int(start_time_list[0]) - 12) + ':' + start_time_list[1] + 'pm'
                else:
                    start_time = str(int(start_time_list[0]) - 12) + 'pm'
            else:
                if int(start_time_list[1]) != 0:
                    start_time = start_time_list[0] + ':' + start_time_list[1] + 'am'
                else:
                    start_time = start_time_list[0] + 'am'

            end_time_list = end.split('T')[1].split('+')[0].split(':')
            if int(end_time_list[0]) > 12:
                if int(end_time_list[1]) != 0:
                    end_time = str(int(end_time_list[0]) - 12) + ':' + end_time_list[1] + 'pm'
                else:
                    end_time = str(int(end_time_list[0]) - 12) + 'pm'
            else:
                if int(end_time_list[1]) != 0:
                    end_time = end_time_list[0] + ':' + end_time_list[1] + 'am'
                else:
                    end_time = end_time_list[0] + 'am'

            meetup = start_time + ' - ' + end_time + ' ' + event['summary']
            print(meetup)
            speak(meetup)
    except HttpError as error:
        print('An error occurred: %s' % error)



def get_day(weekday, next):
    weekday = WEEKDAYS.get(weekday)
    print(weekday)
    dif = weekday - today.weekday()
    date = None
    if dif == 0:
        if next:
            delta = datetime.timedelta(days=7)
            print(delta)
            date = today.date() + delta
            print(date)
        else:
            date = today.date()
            print(date)
    elif dif > 0:
        if next:
            delta = datetime.timedelta(days=dif+7)
            print(delta)
            date = today.date() + delta
            print(date)
        else:
            delta = datetime.timedelta(days=dif)
            print(delta)
            date = today.date() + delta
            print(date)
    elif dif < 0:
        if next:
            delta = datetime.timedelta(days=14 + dif)
            print(delta)
            date = today.date() + delta
            print(date)
        else:
            delta = datetime.timedelta(days=7+dif)
            print(delta)
            date = today.date() + delta
            print(date)

    return date


def get_date(text):
    month = None
    num = None
    year = None
    next = False

    for word in text.split():
        if word == 'today':
            date = datetime.datetime(year=today.year, month=today.month, day=today.day)
            return date.date()
        if word == 'tomorrow':
            date = datetime.datetime(year=today.year, month=today.month, day=today.day + 1)
            return date.date()
        if word == 'next':
            next = True
        if word in WEEKDAYS.keys():
            return get_day(word, next)
        if word in MONTHS.keys():
            month = MONTHS.get(word)
        for ext in DAY_EXT:
            if word.find(ext):
                if word.split(ext)[0].isdigit():
                    num = int(word.split(ext)[0])

    if month < today.month:
        year = today.year + 1
    else:
        year = today.year

    if month and num:
        date = datetime.datetime(year=year, month=month, day=num)
        print(date.date())
        return date.date()


def create_event(summary, date, start_time, end_time):
    local = pytz.timezone('Asia/Almaty')

    event = {
        'summary': summary,
        'start': {
            'dateTime': datetime.datetime.combine(date, datetime.time(int(start_time),0)).astimezone(local).isoformat(),
        },
        'end': {
            'dateTime': datetime.datetime.combine(date, datetime.time(int(end_time),0)).astimezone(local).isoformat(),
        }
    }

    event = SERVICE.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    speak('Event created' + event['summary'])