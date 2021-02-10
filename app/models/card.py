from app.server import db
from datetime import datetime


class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(80), nullable=False)
    question = db.Column(db.String(160), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    typ = db.Column(db.String(10), nullable=False)
    auth_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, topic, question, author, typ):
        self.topic = topic
        self.question = question
        self.typ = typ
        self.author = author
