from datetime import datetime
from flask_login import UserMixin
from app.models import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(160), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    cards = db.relationship('Cards', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def register(email, password):
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
