from . import db
from abc import ABCMeta, abstractmethod

__author__ = 'wissem'

class MyBaseModel:

    __metaclass__ = ABCMeta

    @abstractmethod
    def to_dict(self):
        pass

"""class Question(db.Model, MyBaseModel):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), index=False, unique=False)
    answers = db.Column(db.String(500), index=False, unique=False)
    solutionIndex = db.Column(db.Integer)
    tags = db.Column(db.String(200), index=False, unique=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Question %r>' % (self.question)

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answers': self.answers,
            'solutionIndex': self.solutionIndex,
            'tags': self.tags,
            'owner': User.query.get(self.owner).nickname
        }
"""



class User(db.Model, MyBaseModel):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=False, unique=False )
    email = db.Column(db.String(120), index=True, unique=True)
    token = db.Column(db.String(500))
    #user_questions = db.relationship('Question', backref='author', lazy='dynamic')
    user_mp_hash = db.Column(db.String(200))

    def __init__(self, nickname=None, email=None, token=None, user_mp_hash=None):
        self.nickname = nickname
        self.email = email
        self.token = token
        self.user_mp_hash = user_mp_hash

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def to_dict(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'email': self.email,
            'token': self.token,
            'user_mp_hash': self.user_mp_hash
            #'user_questions': [q.to_dict() for q in self.user_questions]
        }




