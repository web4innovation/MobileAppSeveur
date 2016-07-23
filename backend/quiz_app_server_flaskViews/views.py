from flask import render_template, jsonify, flash, redirect, request, make_response
from . import app, db
from . import models
import hashlib
import numpy as np


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/api/register', methods=['POST'])
def register():
    r = request.get_json()
    user_nickname = str(r['nickname'])
    user_email = str(r['email'])
    user_pass = str(r['pass'])
    user_pass_hash = hashlib.sha1(user_pass.encode('utf-8')).hexdigest()
    user_token = hashlib.sha1(user_pass_hash.encode('utf-8')).hexdigest()
    try:
        u = models.User(nickname=user_nickname, email=user_email, token=user_token, user_mp_hash=user_pass_hash)
        db.session.add(u)
        db.session.commit()
        status = {'token': u.token}
        code = 201
    except Exception as e:
        print(e)
        status = 'this user is already registered'
        code = 401

    return make_response(jsonify({'result': status}), code)


@app.route('/api/authenticate', methods=['POST'])
def authenticate():

    json_data = request.get_json()
    user = models.User.query.filter_by(email=json_data['email']).first()
    print (json_data['email'])
    if user and hashlib.sha1(str(json_data['pass']).encode('utf-8')).hexdigest() == user.user_mp_hash:
        status = {'token': user.token}
        code = 200
    else:
        status = {'result': 'denied'}
        code = 403
    return make_response(jsonify({'result': status}), code)


@app.route('/api/question/random', methods=['GET'])
def get_random_question():

    q_ids = models.Question.query.with_entities(models.Question.id).all()
    to_select = np.random.randint(low=1, high=len(q_ids)+1)
    q = models.Question.query.get(to_select)
    return make_response(jsonify(q.to_dict()),200)


@app.route('/api/question', methods=['POST'])
def add_new_question():

    r = request.get_json()
    email = str(r['email'])
    token = str(r['token'])
    user = models.User.query.filter_by(email=email).first()
    if user and token==user.token:  # user is authenticated then can add the question
        question = str(r['question'])
        q_type = r['question_type']
        answers = r['answers']
        q = models.Question(question=question, question_type=q_type, author=user)
        db.session.add(q)
        db.session.commit()
        for a in answers:
            ans_text = a['answer_text']
            correct = a['correct']
            ans = models.Answer(answer_text=ans_text, correct=correct, quest=q)
            db.session.add(ans)
            db.session.commit()
        return make_response(jsonify(q.to_dict()),201)
    else:
        return make_response(jsonify({'result': 'denied'}), 403)


@app.route('/api/question/ownedby/<owner_nickname>', methods=['GET'])
def get_questions_ownedby(owner_nickname):
    print (owner_nickname)
    user = models.User.query.filter_by(nickname=owner_nickname).first()
    if user:
        r = [q.to_dict() for q in user.user_questions]
        print (r)
    else:
        r = []
    return make_response(jsonify({"result":r}), 200)
