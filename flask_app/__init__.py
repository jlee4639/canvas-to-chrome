"""
Made by: Jayden Lee
Last edited: 6/14/2025
Objective: 
"""

from flask import Flask, request, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

#Set flask_session to db
app.config["SESSION_SQLALCHEMY"] = db

sess = Session(app)

with app.app_context():
    db.create_all()


from flask_app import routes




