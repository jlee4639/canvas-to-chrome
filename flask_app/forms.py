from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CanvasForm(FlaskForm):
    canvas_access_token = StringField("Canvas Access Token", validators=[DataRequired()])
    canvas_url = StringField("Canvas URL", validators=[DataRequired()])
    submit = SubmitField("Import Canvas Calendar")