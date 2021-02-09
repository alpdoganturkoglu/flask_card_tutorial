from app.server import db
from datetime import datetime
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(160), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    cards = db.relationship('Cards', backref='author', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = password