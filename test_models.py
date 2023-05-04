from unittest import TestCase

from app import app 
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):

    def setUp(self):
        """Clean existing users"""
        User.query.delete()

    def tearDown(self):
        """Clean up transactions"""
        db.session.rollback()

    def test_add_user(self):
        user = User(first_name='Test', last_name='User')
        db.session.add(user)
        db.session.commit()

        check_user = User.query.filter_by(first_name='Test').all()
        
        self.assertEqual(check_user, [user])

    

    