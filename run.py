from canvas_api import CanvasAPI
from google_api import GoogleCalendarRequest
import dateutil
import json

#Run flask app
from flask_app import app

#Testing to see if canvas_api and google_api work
def main():
    cur = CanvasAPI("1133~JzQc6thTnyLNvU77kQ9xzcvkHQkeWHTxzaTAMUChKG9UKv2BFTNyutCVvDtMfe4r", "umd.instructure.com")
    current = cur.get_course_id("None", True)
    courses = [(course["name"], course["id"]) for course in current]
    assign = cur.get_assignments()
    #print(assign)
    #print(type(assign))

    #Find calendarID in settings
    #goog = GoogleCalendarRequest("d2c031cac79dd0f5b90ca8f3f5f2adff25a8e50538f5ab44d13ff671ab128b84@group.calendar.google.com")

if __name__ == "__main__":
    main()