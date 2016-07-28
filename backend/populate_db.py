#!flask/bin/python3

from quiz_app_server_flaskViews import app, db, models
import hashlib



__author__ = 'wissem'
from json import *


my_json_data = open('/Users/wissem/Desktop/sweng_question2.json')
my_json_array = load(my_json_data)
# create a new user and call it web4inno_geo_addict
#user_pass = "w4i_is_awesome"
#user_pass_hash = hashlib.sha1(user_pass.encode('utf-8')).hexdigest()
#user_token = hashlib.sha1(user_pass_hash.encode('utf-8')).hexdigest()
#user = models.User(nickname="web4inno_geo_addict", email="w4i@tunes.com", token=user_token, user_mp_hash=user_pass_hash)
#db.session.add(user)
#db.session.commit()
user = models.User.query.filter_by(nickname='web4inno_geo_addict').first()
for json_question in my_json_array:
    question = str(json_question['question'])
    q_type = False
    answers = json_question['answers']
    # add the question to the database
    q = models.Question(question=question, question_type=q_type, author=user)
    db.session.add(q)
    db.session.commit()
    # add answers to the database and refer the question just added
    for i, a in enumerate(answers):
        correct = False
        if i == json_question["solutionIndex"]:
            correct = True
        ans = models.Answer(answer_text=a, correct=correct, quest=q)
        db.session.add(ans)
        db.session.commit()
        # tag the question i.e. add the tags to the database if necessary then refer them to the question
        tags = json_question['tags']
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
