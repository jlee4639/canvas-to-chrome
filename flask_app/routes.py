import json
import os

from flask_app import app
from flask_app.forms import CanvasImportForm, CanvasExportForm
from flask import render_template, flash, redirect, url_for, session, request
from flask_session import Session

from canvas_api import CanvasAPI
from google_api import GoogleCalendarRequest

#Homepage
@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Jayden"}
    return render_template("index.html", user=user)

#Route to import canvas data 
@app.route("/canvas_import", methods=["GET", "POST"])
def canvas_import():
    #Create the import form
    canvas_import_form = CanvasImportForm()

    #Get user canvas info if validation was successful
    if canvas_import_form.validate_on_submit():
        #Get user canva assignments
        user_canvas = CanvasAPI(canvas_import_form.canvas_access_token.data,
                           canvas_import_form.canvas_url.data)
        user_canvas.get_course_id("None", True)
        user_canvas_assignments = user_canvas.get_assignments()
        
        #Store users canvas info in sesssion to use in the redirect
        session["user_canvas_assignments"] = user_canvas_assignments
        
        #Redirect to canvas_export page
        return redirect(url_for("canvas_export"))
    
    #Load initial page
    return render_template("canvas_import.html",
                           title="Import Canvas Calendar",
                           import_form=canvas_import_form)

#Route to show calendar and export assignment data to Google Calendar
@app.route("/canvas_export", methods=["GET", "POST"])
def canvas_export():
    #Retreive user_canvas_data from the server-sided session
    user_canvas_assignments = session.get("user_canvas_assignments")
    #Create import form
    canvas_export_form = CanvasExportForm()
        
    #Get user canvas info if validation was successful
    if canvas_export_form.validate_on_submit():
        #Pop session data
        session.pop("user_canvas_assignments", None)

        #Get filelocation to save service account key file
        DIR = os.path.dirname(os.path.dirname("__file__"))
        sac_path_name = os.path.join(DIR, "service_account_key.json")

        #Get the file input by user and create a json file with service account key data
        sac_file = canvas_export_form.service_account_key.data
        sac_file.save(sac_path_name)

        GoogleCalendarRequest(canvas_export_form.calendar_id.data,
                              canvas_export_form.fullcalendar_events.data)

        #Load Sign-in page for Google calendar
        return redirect("https://workspace.google.com/intl/en-US/products/calendar/")

    return render_template("canvas_export.html",
                           export_form=canvas_export_form,
                           canvas_assignments=user_canvas_assignments)
