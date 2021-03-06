from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    '''connect to database'''
    db.app = app
    db.init_app(app)



"""Models for Blogly."""

class User(db.Model):
    '''user on site'''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)

    first_name = db.Column(db.String(30), nullable = False)

    last_name = db.Column(db.String(30), nullable = False)
    
    # default image taken from unsplash.com
    image_url = db.Column(db.String(500), nullable = False, default = 'https://images.unsplash.com/photo-1503164412421-0512323df4e7?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80')

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    '''site post'''
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.String(1000), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

   

    

class Tag(db.Model):
    '''tag, description of a post'''
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable = False, unique = True)

    posts = db.relationship('Post', secondary='post_tags', backref='tags')




class PostTag(db.Model):
    '''tags on a post'''
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)