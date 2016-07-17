from flask import render_template, jsonify, flash, redirect
from . import app

from .forms import PostQuestionForm


@app.route('/')
@app.route('/index')
def index():
    question = {"tags": [
                  "capitals",
                  "geography",
                  "countries"
                 ],
                 "solutionIndex": 1,
                 "question": "What is the capital of Hungary?",
                 "answers": [
                  "Juba",
                  "Budapest",
                  "San Jos\u00e9",
                  "Lom\u00e9",
                  "Doha",
                  "Hanga Roa",
                  "Yamoussoukro",
                  "Adamstown",
                  "Islamabad",
                  "Charlotte Amalie"
                 ],
                 "owner": "sehaag",
                 "id": 5025935027863552}  # fake question
    return render_template('index.html',
                           title='Home',
                           question=question)


@app.route('/submit_new_question', methods=['GET', 'POST'])
def submit_new_question():
    form = PostQuestionForm()
    if form.validate_on_submit():
        flash('question="%s", answers=%s,  tags=%s' %
              (form.question.data, str(form.answers.data),str(form.tags.data)))
        return redirect('/index')
    return render_template('submit_new_question.html',
                           title='Submit Question Form',
                           form=form)