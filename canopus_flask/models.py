from canopus_flask import db, login_manager
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.sqlite import BLOB
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Integer, default=False)

    def __repr__(self):
        return f'{self.username} : {self.email} : {self.date_created}'


class Carousel(db.Model):
    __tablename__ = "carousel"

    id = db.Column(db.Integer, primary_key=True)
    carousel_name = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f'{self.carousel_name} : {self.user_id}'


class Image(db.Model):
    __tablename__ = "image"

    id = db.Column(db.Integer, primary_key=True)
    carousel_id = db.Column(db.Integer, ForeignKey("carousel.id"), nullable=False)
    image_file = db.Column(BLOB, nullable=False)
    raw_image_name = db.Column(db.String(40), nullable=False)
    image_caption = db.Column(db.String(60), default="No Caption added.")

    def __repr__(self):
        return f'{self.image_file} : {self.carousel_id}'


@login_manager.user_loader
def load_user(user_id):
    print("User_id: ", user_id)
    expected_result = User.query.get(user_id)
    return expected_result
