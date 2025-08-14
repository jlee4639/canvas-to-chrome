from flask_app import app
from flask import render_template, flash, redirect, url_for, session
from flask_app.forms import CanvasForm
from canvas_api import CanvasAPI

#Homepage
@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Jayden"}
    return render_template("index.html", user=user)

#Canvas Form and Calendar Output Page
@app.route("/canvas_import", methods=["GET", "POST"])
def canvas_import():
    user_canvas_assignments = session.pop("user_canvas_assignments", None)
    canvas_form = CanvasForm()

    #Get user canvas info if validation was successful
    if canvas_form.validate_on_submit():
        user_canvas = CanvasAPI(canvas_form.canvas_access_token.data,
                           canvas_form.canvas_url.data)
        #Retreive all user courses
        user_canvas.get_course_id("None", True)

        #Returns all assignments of the user
        user_canvas_assignments = user_canvas.get_assignments()
        
        #Store users canvas info in sesssion to use in the redirect
        session["user_canvas_assignments"] = user_canvas_assignments
        
        return redirect(url_for("canvas_import"))
    
    return render_template("canvas_import.html",
                           title="Import Canvas Calendar",
                           form=canvas_form,
                           canvas=user_canvas_assignments)