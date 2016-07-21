from flask import render_template, jsonify, flash, redirect, request, make_response
from . import app, db
from . import models
import hashlib


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
        u = models.User(user_nickname, user_email, user_token, user_pass_hash)
        db.session.add(u)
        db.session.commit()
        status = {'token': u.token}
        code = 201
    except:
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





