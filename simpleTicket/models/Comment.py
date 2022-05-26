from db import db
from datetime import datetime
from typing import List


class CommentModel(db.Model):
    __tablenames__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    email = db.Column(db.String(50), unique=True)
    text = db.Column(db.String(), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)

    def __init__(self, email, text, ticket_id):
        self.email = email
        self.text = text
        self.ticket_id = ticket_id

    def __repr__(self):
        return 'CommentModel(email=%s, text=%s, ticket_id=%s)' % (self.email, self.text, self.ticket_id)

    def json(self):
        return {'email': self.email, 'text': self.text}

    @classmethod
    def find_by_id(cls, _id) -> 'CommentModel':
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List['CommentModel']:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()