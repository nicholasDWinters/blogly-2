from unittest import TestCase

from app import app
from models import db, User

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
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Nick Winters', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.user.first_name, html)
            self.assertIn(self.user.last_name, html)
          
            

    def test_add_user(self):
        with app.test_client() as client:
            # image url taken from unsplash.com
            data = {"first_name": "John", 'last_name': 'Winters', 'image_url':'https://images.unsplash.com/photo-1616171812687-1028c744649d?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80'}
            resp = client.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/users/2">John Winters</a></li>', html)

    def test_delete_user(self):
           with app.test_client() as client:
            # image url taken from unsplash.com
            data = {"first_name": "John", 'last_name': 'Winters', 'image_url':'https://images.unsplash.com/photo-1616171812687-1028c744649d?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80'}
            resp = client.post(f"/users/{self.user_id}/delete", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f"<li><a href='/users/{self.user_id}'>John Winters</a></li>", html)
            self.assertEqual(User.query.filter_by(id = self.user_id).one_or_none(), None)