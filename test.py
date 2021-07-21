from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyTestCase(TestCase):
    """Test Blogly"""
    def setUp(self):
        """Add sample user and post"""
        Post.query.delete()
        User.query.delete()

        user = User(first_name="Spongebob", last_name="Squarepants", image_url="https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/SpongeBob_SquarePants_character.svg/1920px-SpongeBob_SquarePants_character.svg.png")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        post = Post(title="The Krabby Patty Formula", content="Just kidding Plankton! I would never upload the secret formula for the whold world to see! You've been foiled again!", user_id = self.user_id)

        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.post = post
    
    def tearDown(self):
        """Get rid of any unwanted changes"""
        db.session.rollback()
    
    """Test views for User"""
    def test_list_users(self):
        """Testing showing list of users"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Spongebob', html)
    
    def test_show_user_info(self):
        """Testing showing user info"""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Spongebob Squarepants</h1>', html)

    def test_show_new_user_form(self):
        """Test showing the user form"""
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a User', html)

    def test_add_new_user(self):
        """Test adding new user"""
        with app.test_client() as client:
            data = {"first_name": "Patrick", "last_name": "Star", "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/3/33/Patrick_Star.svg/1920px-Patrick_Star.svg.png"}
            
            resp = client.post('/users/new', data = data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Patrick Star', html)

    """Test views for posts"""
    def test_new_post(self):
        """Test adding new post"""
        with app.test_client() as client:
            data = {"title": "OH SQUIIIIIIIDWAAAAARRRRRRDDD", "content": "Patrick and I are blowing bubbles! Wanna join?"}
            resp = client.post(f'/users/{self.user_id}/posts/new', data = data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('OH SQUIIIIIIIDWAAAAARRRRRRDDD', html)
    
    def test_show_post(self):
        """Test show post"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('The Krabby Patty Formula', html)

    def test_edit_post(self):
        """Test edit post"""
        with app.test_client() as client:
            data = {"title": "The Krabby Patty Formula", "content": "The secret formula is you, Plankton. Run away."}
            resp = client.post(f'/posts/{self.post_id}/edit', data = data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.post.content, 'The secret formula is you, Plankton. Run away.')
    
    def test_delete_post(self):
        """Test delete post"""
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Post The Krabby Patty Formula successfully deleted', html)