"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_IMAGE_URL = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'

class User(db.Model):

    __tablename__ = "users"

    def __repr__(self):
        return f'<User id={self.id} first_name={self.first_name} last_name={self.last_name} image_url={self.image_url}>'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False, unique=True)
    last_name = db.Column(db.String, nullable=False, unique=True)
    image_url = db.Column(db.String, nullable=False, default=DEFAULT_IMAGE_URL) 

    posts = db.relationship('Post', backref='users')


class Post(db.Model):

    __tablename__ = 'posts'

    def __repr__(self):
        return f'<Post id={self.id} Title={self.title} Content={self.content} Created at{self.created_at} User Id={self.user_id}>'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Tag(db.Model):

    __tablename__ = 'tags'

    def __repr__(self):
        return f'<Tag id={self.id} Name={self.name}>'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='post_tags', backref='tags')


class PostTag(db.Model):

    __tablename__ = 'post_tags'

    def __repr__(self):
        return f'<Post Id={self.post_id} Tag Id={self.tag_id}'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)