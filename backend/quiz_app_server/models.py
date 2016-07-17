from . import db

__author__ = 'wissem'


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), index=False, unique=False)
    answers = db.Column(db.String(500), index=False, unique=False)
    solutionIndex = db.Column(db.Integer)
    tags = db.Column(db.String(200), index=False, unique=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Question %r>' % (self.question)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=False, unique=False )
    email = db.Column(db.String(120), index=True, unique=True)
    user_questions = db.relationship('Question', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)
