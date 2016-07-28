from flask import render_template, jsonify, flash, redirect, request, make_response
from . import app, db
from . import models
import hashlib
import numpy as np
from sqlalchemy import func


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/api/register', methods=['POST'])
def register():
    """

    :return:
    """
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
        status = 'email or nickname already exist'
        code = 401

    return make_response(jsonify({'result': status}), code)


@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    """

    :return:
    """
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
    """

    :return:
    """
    q_ids = models.Question.query.with_entities(models.Question.id).all()
    to_select = np.random.randint(low=1, high=len(q_ids)+1)
    q = models.Question.query.get(to_select)
    return make_response(jsonify(q.to_dict()),200)


@app.route('/api/question', methods=['POST'])
def add_new_question():
    """

    :return:
    """
    r = request.get_json()
    email = str(r['email'])
    token = str(r['token'])
    user = models.User.query.filter_by(email=email).first()
    if user and token==user.token:  # user is authenticated then can add the question
        question = str(r['question'])
        q_type = r['question_type']
        answers = r['answers']
        # add the question to the database
        q = models.Question(question=question, question_type=q_type, author=user)
        db.session.add(q)
        db.session.commit()
        # add answers to the database and refer the question just added
        for a in answers:
            ans_text = a['answer_text']
            correct = a['correct']
            ans = models.Answer(answer_text=ans_text, correct=correct, quest=q)
            db.session.add(ans)
            db.session.commit()
        # tag the question i.e. add the tags to the database if necessary then refer them to the question
        tags = r['tags']
        for t in tags:
            try:
                q_tag = models.Tag.query.filter_by(tag_name=t).first()
                if q_tag is None:
                    q_tag = models.Tag(tag_name=t)
                    db.session.add(q_tag)
                q.tags.append(q_tag)
                db.session.commit()
            except Exception as e:
                print ("tag not registered")
                pass

        return make_response(jsonify(q.to_dict()),201)
    else:
        return make_response(jsonify({'result': 'denied'}), 403)


@app.route('/api/question/ownedby/<owner_nickname>', methods=['GET'])
def get_questions_ownedby(owner_nickname):
    """

    :param owner_nickname:
    :return:
    """
    print (owner_nickname)
    user = models.User.query.filter_by(nickname=owner_nickname).first()
    if user:
        r = [q.to_dict() for q in user.user_questions]
        print (r)
    else:
        r = []
    return make_response(jsonify({"result":r}), 200)


@app.route('/api/question/bytag/<tag_name>', defaults={'limit':1}, methods=['GET'])
@app.route('/api/question/bytag/<tag_name>/<limit>')
def get_question_bytag(tag_name,limit):
    """

    :param tag_name:
    :return:
    """
    print(tag_name)
    max_questions=20
    tag = models.Tag.query.filter_by(tag_name=tag_name).first()
    if tag:
        try:
            limit = int(limit)
        except Exception as e:
            pass
        if isinstance(limit,int):
            if limit > max_questions or limit <=0:
                limit=max_questions
            questions = tag.quest.order_by(func.random()).limit(limit).all()
        elif limit=='all':
            questions = tag.quest.all()
        else:
            questions = []
        r = [q.to_dict() for q in questions]
    else:
        r = []
    return make_response(jsonify({"result":r}), 200)


@app.route('/api/tags', methods=['GET'])
def get_tag_list():
    """

    :param tag_name:
    :return:
    """

    tags = models.Tag.query.all()
    if tags:

        r = [t.to_dict() for t in tags]
    else:
        r = []
    return make_response(jsonify({"result":r}), 200)
