from . import db
from abc import ABCMeta, abstractmethod

__author__ = 'wissem'


tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('q_id', db.Integer, db.ForeignKey('question.id')))


class MyBaseModel:

    __metaclass__ = ABCMeta

    @abstractmethod
    def to_dict(self):
        pass


class Question(db.Model, MyBaseModel):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), index=False, unique=False)
    answers = db.relationship('Answer', backref='quest', lazy='dynamic')
    question_type = db.Column(db.Boolean)  # True means multiple choice, False means single answer
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('quest', lazy='dynamic'))

    def __repr__(self):
        return '<Question %r>' % (self.question)

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answers': [a.to_dict() for a in self.answers],
            'owner': self.author.nickname,
            'multiple_choice': self.question_type,
            'tags': [t.tag_name for t in self.tags]
        }


class User(db.Model, MyBaseModel):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=False, unique=False )
    email = db.Column(db.String(120), index=True, unique=True)
    token = db.Column(db.String(500))
    user_questions = db.relationship('Question', backref='author', lazy='dynamic')
    user_mp_hash = db.Column(db.String(200))

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def to_dict(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'email': self.email,
            'token': self.token,
            'user_mp_hash': self.user_mp_hash
        }


class Answer(db.Model, MyBaseModel):
    id = db.Column(db.Integer, primary_key=True)
    q_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_text = db.Column(db.String(200))
    correct = db.Column(db.Boolean)

    def __repr__(self):
        return '<Answer %r,%s>' % (self.answer_text,self.correct)

    def to_dict(self):
        return {
            'answer_text': self.answer_text,
            'correct': self.correct
        }


class Tag(db.Model, MyBaseModel):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<Tag %r,%s>' % (self.id, self.tag_name)

    def to_dict(self):
        return {
            'id': self.id,
            'tag_name': self.tag_name
        }
