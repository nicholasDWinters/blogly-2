"""Blogly application."""

from flask import Flask, request, request, render_template, flash, session
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'oh-so-secret'

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    return render_template('index.html')