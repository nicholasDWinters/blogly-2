from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()
        
        # image url taken from unsplash.com
        user = User(first_name="Nick", last_name='Winters', image_url = 'https://images.unsplash.com/photo-1587063041428-6ce2ab071644?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=385&q=80')

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user
       

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        '''tests users routes to make sure users are displayed correctly in the list'''
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Nick Winters', html)

    def test_show_user(self):
        '''tests show route, should display specified user information'''
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.user.first_name, html)
            self.assertIn(self.user.last_name, html)
          
            

    def test_add_user(self):
        '''tests add user route to make sure correct info is displayed and user is added to database'''
        with app.test_client() as client:
            # image url taken from unsplash.com
            data = {"first_name": "John", 'last_name': 'Winters', 'image_url':'https://images.unsplash.com/photo-1616171812687-1028c744649d?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80'}
            resp = client.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/users/2">John Winters</a></li>', html)

    def test_edit_user(self):
        '''tests edit route, should allow a user to be edited and saved to database'''
        with app.test_client() as client:
            # image taken from unsplash.com
            data = {"first_name": "John", 'last_name': 'Winters', 'image_url':'https://images.unsplash.com/photo-1616171812687-1028c744649d?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80'}

            resp = client.post(f'/users/{self.user_id}/edit', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            
            self.assertIn('<li><a href="/users/1">John Winters</a></li>', html)
            self.assertNotIn('<li><a href="/users/1">Nick Winters</a></li>', html)
            
            

    def test_delete_user(self):
        '''tests delete post route, user should no longer be displayed in html'''
        with app.test_client() as client:
            # image url taken from unsplash.com
            data = {"first_name": "John", 'last_name': 'Winters', 'image_url':'https://images.unsplash.com/photo-1616171812687-1028c744649d?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80'}
            resp = client.post(f"/users/{self.user_id}/delete", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f"<li><a href='/users/{self.user_id}'>John Winters</a></li>", html)
            self.assertEqual(User.query.filter_by(id = self.user_id).one_or_none(), None)

    
class PostViewsTestCase(TestCase):
    """Tests for views for Posts."""

    def setUp(self):
        """Add sample user and post."""

        User.query.delete()
        Post.query.delete()
        # image url taken from unsplash.com
        user = User(first_name="Nick", last_name='Winters', image_url = 'https://images.unsplash.com/photo-1587063041428-6ce2ab071644?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=385&q=80')

        post = Post(title='Test Post', content='Test post content', user_id = 1)
        db.session.add(user)
        db.session.add(post)
        db.session.commit()

        

        self.user_id = user.id
        self.user = user
        self.post_id = post.id
        self.post = post

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_show_posts(self):
        '''tests show user route, should display specified user post titles as well'''
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.post.title, html)
           
    def test_add_post(self):
        '''tests add post route to make sure correct info is displayed and post is added to database'''
        with app.test_client() as client:
            
            data = {"title": "Second Post", 'content': 'second post content'}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a class="noDecoration" href="/posts/2">Second Post</a></li>', html)

    def test_edit_post(self):
        '''tests edit post route, should allow a post to be edited and saved to database'''
        with app.test_client() as client:
           
            data = {"title": "Second Post", 'content': 'second post content'}

            resp = client.post(f'/posts/{self.post_id}/edit', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            
            self.assertIn('<h5 class="mt-3">second post content</h5>', html)
            self.assertNotIn('<h5 class="mt-3">Test post content</h5>', html)

    def test_delete_post(self):
        '''tests delete post route, post should no longer be displayed in html'''
        with app.test_client() as client:
            
            data = {"title": "Second Post", 'content': 'second post content'}

            resp = client.post(f"/posts/{self.post_id}/delete", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('<li><a class="noDecoration" href="/posts/2">Second Post</a></li>', html)
            self.assertEqual(Post.query.filter_by(id = self.post_id).one_or_none(), None)