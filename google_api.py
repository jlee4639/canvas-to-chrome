"""
Made by: Jayden Lee
Last edited: 6/14/2025
Objective: Get a user's Canvas instructure API token to access their courses, assignments,
discussions, and quizzes and imports it to Google Calendar
"""

import datetime
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendarRequest:
    _SCOPES = ["https://www.googleapis.com/auth/calendar"] #Permissions for Google Calendar
    _CUR_DIR = os.path.dirname(os.path.abspath(__file__)) #Absolute file path for this current file
    _CREDS_PATH = os.path.join(_CUR_DIR, "../credential.json") #Get file path for credentials relative to CUR_DIR
    

    def __init__(self):
        print(f"Scope: {self._SCOPES}, Cur_Dir: {self._CUR_DIR}, Creds Path: {self._CREDS_PATH}")
        #Hold user's OAuth2 credentials
        self._creds = None

        #Check if credentials have been saved so user doesn't need to sign in each time
        if os.path.exists("token.json"):
            self._creds = Credentials.from_authorized_user_file("token.json")
        
        #Check if credentials are missing or invalid
        if not self._creds or not self._creds.valid:
            #Refresh expired tokens
            if self._creds and self._creds.expired and self._creds.refresh_token:
                self._creds.request(Request())
            #First-time login
            else:
                self._flow = InstalledAppFlow.from_client_secrets_file(self._CREDS_PATH, self._SCOPES)
                #Opens up webpage to login
                self._creds = self._flow.run_local_server(port = 5000)

            #Save new token in token.json
            with open("token.json", "w") as token:
                token.write(self._creds.to_json())

        #Create a client for the Calendar API v3
        try:
            self._service = build("calendar", "v3", credentials = self._creds)

            now = datetime.datetime.now().isoformat() + "Z"

            event_result = self._service.events().list(calendarId = "primay", timeMin = now, maxResults = 10, singleEvents = True, orderBy = "startTime")
            events = event_result.get("items", [])

            if not events:
                print("No upcoming events")
            else:
                for event in events:
                    start = event["start"].get("dateTime", event["start"].get("date"))
                    print(start, event["summary"])

        except HttpError as error:
            print(f"HTTP Error has occured: {error}")