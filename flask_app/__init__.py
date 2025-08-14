"""
Made by: Jayden Lee
Last edited: 6/14/2025
Objective: 
"""

from flask import Flask, request, render_template
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from flask_app import routes




