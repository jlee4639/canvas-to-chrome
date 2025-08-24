from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, HiddenField, FileField
from wtforms.validators import DataRequired


class CanvasImportForm(FlaskForm):
    canvas_access_token = StringField("Canvas Access Token", validators=[DataRequired()], render_kw={"class": "form_input"})
    canvas_url = StringField("Canvas URL", validators=[DataRequired()], render_kw={"class": "form_input"})
    submit = SubmitField("Import Canvas Assignments", render_kw={"class": "submit"})

class CanvasExportForm(FlaskForm):
    calendar_id = StringField("Calendar ID", validators=[DataRequired()], render_kw={"class": "form_input"})
    service_account_key = FileField("Service Account Key File", validators=[FileRequired(), FileAllowed(["json"], "JSON Files only")])
    fullcalendar_events = HiddenField("FullCalendar Events")
    submit = SubmitField("Export Canvas Assignments", render_kw={"class": "submit"})