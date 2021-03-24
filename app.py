"""Blogly application."""

from flask import Flask, request, request, render_template, flash, session, redirect
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
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/create')
def create_user():
    return render_template('create.html')

@app.route('/create', methods=['POST'])
def add_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    if request.form['image_url']:
        image_url = request.form['image_url']
    else:
        image_url = None

    user = User(first_name=first_name.capitalize(), last_name=last_name.capitalize(), image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect('/')

@app.route('/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('show.html', user=user)