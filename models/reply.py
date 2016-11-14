import time
from datetime import datetime

from app import db
from models.user import User
from models.message import Message

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255), unique=True)
    datetime = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('messages', lazy='dynamic'))

    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    message = db.relationship('Message',
        backref=db.backref('replies', lazy='dynamic'))

    def __init__(self, user_id, message_id, body):
        self.body = body
        self.user_id = user_id
        self.message_id = message_id

        self.datetime = datetime.utcnow()


    def to_dict(self):
        output = {}
        output["id"] = self.id
        output["body"] = self.body
        output["user"] = self.user.to_dict()
        output["message"] = self.message.to_dict()

        return output

    def __str__(self):
        return "'<Reply %r>' % self.id"
