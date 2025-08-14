"""
Made by: Jayden Lee
Last edited: 6/14/2025
Objective: Get a user's Canvas instructure API token to access their courses, assignments,
discussions, and quizzes and imports it to Google Calendar
"""

import requests
from datetime import datetime, timezone

class CanvasAPI:
    def __init__(self, access_token = None, base_url = None):
        #Need access token to get data from Canvas
        if not access_token:
            raise ValueError("No access token was provided")
        
        #Need to have canvas url to get data from Canvas
        if not base_url:
            raise ValueError("No Canvas URL")
        
        self._access_token = access_token
        self._base_url = f"https://{base_url}"

        #Token for Canvas API
        self._headers = {
            "Authorization": f"Bearer {self._access_token}"
        }

        #Meta data about current user courses, assignments, quizzes, and discussions
        self._current_courses = [] #List of user's current course
        self._current_assignments = [] #Lists all of the user's graded assignments


    """
    This helper function is used to send a HTTP request to the Canvas API. endpoint param
    is the specific end url to get the API data (courses or assignments). params param is
    used to specify the data you want from the API. The function returns an array of json 
    files of the data requested front he specified endpoint.
    """
    def _get_request(self, endpoint, params = None):
        url = f"{self._base_url}/api/v1/{endpoint}"
        data = []

        #Loop through every page in url
        while url:
            #Send HTTP get request to Canvas API
            response = requests.get(
                url,
                params = params,
                headers = self._headers
            )

            #Check for errors in the request
            if response.status_code != 200:
                raise Exception(f"Failed to get Canvas Course ID: {response.status_code}. Error Reason: {response.reason}")

            data.extend(response.json())

            url = response.links.get("next", {}).get('url')       
            params = None

        return data


    """
    This helper function gets all the current courses the user has. This will be used to 
    get all the assignments, discussions, and quizzes from the Canvas Calendar Events.
    term argument is used to determine the term of classes to filter. If term is "Null",
    will not be used. isFavorite argument is used to filter favorited courses. True is
    only use favorited classes and false is favorited classes doesn't matter
    """
    def get_course_id(self, term, isFavorite):
        #Get user courses information
        courses = self._get_request(
            "courses",
            {
                "include[]": ["term", "favorites"],
                "state[]": ["completed", "created", "available"],
                "per_page": 100
            })

        #Courses after filtering by favorite and term
        filtered_courses = []

        #Filter out courses by term and favorites
        
        for course in courses:
            add = True

            #If isFavorite is true and course is not favorited
            if isFavorite and not(course.get("is_favorite", False)):
                add = False
            
            #If term isnt None and course term doesnt match with arg term
            if (term != "None") and (term != course.get("term", {}).get("name", {})):
                add = False

            #Add if course matches params
            if add:
                filtered_courses.append(course)
        
        self._current_courses = filtered_courses
        

        return filtered_courses


    """
    This function gets the user's course assignments from the Canvas Instructure API, retreiving info including
    assignment name, course name, assignment id, and start and end date. Returns a list of dicts used to add events
    into the FullCalendar implementation
    """
    def get_assignments(self):
        #Loop through each course in _current_courses
        for course in self._current_courses:
            print(course["id"])
            assignments  = self._get_request(
                f"courses/{course['id']}/assignments",
                params = {
                    "per_page": 100
                }
            )

            #Get course name, title, due date, and description for each assignment
            #Name matches event object for FullCalendar.io import
            for assignment in assignments:
                assign_date = {
                    "title": assignment.get("name"),
                    "groupId": course["name"],
                    "id": assignment.get("id"),
                    #Set to datetime.now(timezone.utc).isoformat()
                    "start": "2025-01-12T00:00:00Z",
                    "end": assignment.get("due_at"),
                }

                #Holds all data for course assignments
                self._current_assignments.append(assign_date)

        return self._current_assignments