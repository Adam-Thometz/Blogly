from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """Test views for User"""
    def setUp(self):
        """Add sample user"""

        User.query.delete()

        user = User(first_name="Spongebob", last_name="Squarepants", image_url="https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/SpongeBob_SquarePants_character.svg/1920px-SpongeBob_SquarePants_character.svg.png")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user
    
    def tearDown(self):
        """Get rid of any unwanted changes"""
        db.session.rollback()
    
    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Spongebob', html)
    
    def test_show_user_info(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Spongebob Squarepants</h1>', html)

    def test_show_new_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a User', html)

    def test_add_new_user(self):
        with app.test_client() as client:
            data = {"first_name": "Patrick", "last_name": "Star", "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/3/33/Patrick_Star.svg/1920px-Patrick_Star.svg.png"}
            
            resp = client.post('/users/new', data = data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Patrick Star', html)