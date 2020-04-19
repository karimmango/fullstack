from datetime import datetime
from blog import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(100), nullable=False, unique=True)
    email= db.Column(db.String(120), nullable=False, unique=False)
    password= db.Column(db.String(120), nullable=False)
    profile_pic=db.Column(db.String(120), nullable=False, default='default.jpg')
    posts=db.relationship('Post', backref='author', lazy=True)
    biography=db.Column(db.Text, nullable=True)
    def __repr__(self):
        return f"User ('{self.username}', '{self.email}, '{self.biography}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

