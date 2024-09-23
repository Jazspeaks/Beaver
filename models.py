
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    cv = db.relationship('CV', backref='owner', lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)

class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    job_title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    education = db.Column(db.PickleType, default=[])
    experience = db.Column(db.PickleType, default=[])
    projects = db.Column(db.PickleType, default=[])
    skills = db.Column(db.PickleType, default=[])
    certifications = db.Column(db.PickleType, default=[])
    interests = db.Column(db.PickleType, default=[])
    references = db.Column(db.PickleType, default=[])

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    media = db.Column(db.String(120), nullable=True)  # For storing the media filename
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user = db.relationship('User', backref='comments') 
