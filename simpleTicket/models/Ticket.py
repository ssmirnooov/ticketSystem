from db import db
from typing import List
from datetime import datetime


class TicketModel(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    topic = db.Column(db.String(100), unique=True)
    text = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(50), unique=True)
    status = db.Column(db.String(10), default='Opened')

    comments = db.relationship('CommentModel', backref='ticket_list', lazy=True, primaryjoin='TicketModel.id == CommentModel.ticket_id')

    def __init__(self, topic, text, email):
        self.topic = topic
        self.text = text
        self.email = email

    @classmethod
    def __repr__(self):
        return 'TicketModel(name=%s)' % self.topic

    @classmethod
    def find_by_id(cls, _id) -> "TicketModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_topic(cls, topic) -> "TicketModel":
        return cls.query.filter_by(topic=topic).first()

    @classmethod
    def find_all(cls) -> List['TicketModel']:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
