from urllib import response
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES = []
COUNT = 0

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get('/')
def display_survey():
    return render_template("survey_start.html")

@app.get(f'/questions/{COUNT}')
def show_questions():
    question = survey.questions[COUNT].question
    choices = survey.questions[COUNT].choices
    return render_template("question.html", question = question, choices = choices)

@app.post('/answer')
def get_answer():
    response = request.form["answer"]
    RESPONSES.append(response)
    COUNT = 1
    return redirect(f'/questions/{COUNT}')
