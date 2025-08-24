"""
Made by: Jayden Lee
Last edited: 6/14/2025
Objective: Get a user's Canvas instructure API token to access their courses, assignments,
discussions, and quizzes and imports it to Google Calendar
"""
import sys
import datetime
import os
import json

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendarRequest:
    _SCOPES = ["https://www.googleapis.com/auth/calendar"] #Permissions for Google Calendar
    _SERVICE_ACCOUNT_KEY = "service_account_key.json" #Absolute file path for this current file
    _EMAIL = None

    """
    The constructor takes in an email address associated with the calendar that the user
    wants to import the Canvas Calendar to. in order for the init to work, users need to
    create a service account on Google Cloud Console and add the service account's gmail to
    their Google Calendar. Also need a service_account_key.json containing the service
    account key in it aswell.
    """
    def __init__(self, calendarId, fullcalendar_events):
        if not calendarId or not fullcalendar_events:
            raise Exception("No email provided")

        creds = None

        if os.path.exists("service_account_key.json"):
            #Get credentials to access User Google calendar with service accounts
            creds = service_account.Credentials.from_service_account_file(self._SERVICE_ACCOUNT_KEY, scopes=self._SCOPES)

        try:
            #Build the user calendar with credentials
            service = build("calendar", "v3", credentials=creds)
            cur_time = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

            fc_events = json.loads(fullcalendar_events)

            #Export data to Google Calendar
            for event in fc_events:
                service.events().insert(calendarId=calendarId, body=event).execute()

        except Exception as error:
            raise Exception(f"HttpError: {error}")