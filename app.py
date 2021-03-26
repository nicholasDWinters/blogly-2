"""Blogly application."""

from flask import Flask, request, request, render_template, flash, session, redirect, url_for
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'oh-so-secret'

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    posts = Post.query.all()
    posts = list(posts)
    posts.reverse()
    posts[:5]
    users = User.query.all()
    return render_template('home.html', posts = posts, users = users)

@app.route('/users')
def users_page():
    '''displays all users'''
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/users/new')
def create_user():
    '''display create a new user form'''
    return render_template('create.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    '''post route to create new user'''
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None

    user = User(first_name=first_name.capitalize(), last_name=last_name.capitalize(), image_url=image_url)
    db.session.add(user)
    db.session.commit()
    flash('Created new user!', 'success')
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    '''display name and image for specified user'''
    user = User.query.get_or_404(user_id)

    return render_template('show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit(user_id):
    '''display edit form for editing the specified user's information'''
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    '''post route for editing user information, saves to db'''
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    if user.image_url:
        user.image_url = user.image_url 
    else:
        # image taken from unsplash.com
        user.image_url = 'https://images.unsplash.com/photo-1503164412421-0512323df4e7?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80'
    

    db.session.add(user)
    db.session.commit()
    flash('Edited user!', 'success')
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    '''route to delete specified user from db'''
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash('Deleted user!', 'error')
        return redirect('/users')
    except:
        flash('Unable to delete user!', 'error')
        return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def add_post(user_id):
    '''show form to add a post'''
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('postForm.html', user = user, tags = tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    '''save post to database'''
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tag')
    
    post = Post(title=title, content=content, user = user)

    for tag in tags:
        tagObj = Tag.query.filter_by(name=tag).all()
        post.tags.append(tagObj[0])

    db.session.add(post)
    db.session.commit()
    flash('Created new post!', 'success')
    return redirect(url_for('.show_user', user_id = user_id))

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    '''render post show page'''
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    
    return render_template('showPost.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    '''render the post edit form'''
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    tags = Tag.query.all()

    return render_template('editPost.html', post = post, user = user, tags = tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def save_edits(post_id):
    '''post route for editing post information, saves to db'''
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tags = request.form.getlist('tag')
    post.tags = []
    for tag in tags:
        tagObj = Tag.query.filter_by(name=tag).all()
        post.tags.append(tagObj[0])

    db.session.add(post)
    db.session.commit()
    flash('Edited post!', 'success')
    return redirect(url_for('.show_post', post_id=post_id))

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    '''route to delete specified post from db'''
    try:
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash('Successfully deleted post!', 'success')
        return redirect('/')
    except:
        flash('Unable to delete post!', 'error')
        return redirect(url_for('.show_post', post_id=post_id))
    


@app.route('/tags')
def tags_page():
    '''displays all tags'''
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    '''display name for tag and associated posts'''
    tag = Tag.query.get_or_404(tag_id)

    return render_template('showTag.html', tag = tag)

@app.route('/tags/new')
def add_tag():
    '''show form to add a tag'''
    return render_template('tagForm.html')

@app.route('/tags/new', methods=['POST'])
def create_tag():
    '''create new tag and save to database'''
    name = request.form['tag_name'] 

    try:
        tag = Tag(name = name)
        db.session.add(tag)
        db.session.commit()
        flash('Created new tag!', 'success')
        return redirect('/tags')
    except:
        flash('Unable to add tag!', 'error')
        return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    '''show edit form for specified tag'''
    tag = Tag.query.get_or_404(tag_id)

    return render_template('editTag.html', tag = tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def save_tag_edits(tag_id):
    '''save the edited tag to database'''
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['tag_name']
    try:
        db.session.add(tag)
        db.session.commit()
        flash('Edited tag!', 'success')
        return redirect('/tags')
    except:
        db.session.rollback()
        flash('Unable to edit tag!', 'error')
        return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    '''delete tag from database'''
    try:
        tag = Tag.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        flash('Successfully deleted tag!', 'success')
        return redirect('/tags')
    except:
        flash('Unable to delete tag!', 'error')
        return redirect('/tags')
    