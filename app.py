from urllib import response
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

SURVEY_ANSWERS = []

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get('/')
def display_survey():
    """ Load homepage with survey title, instructions, and survey start button """

    return render_template("survey_start.html", survey=survey)

@app.get('/questions/<int:count>')
def show_questions(count):
    """ Display question with answer choices as radio buttons """

    # session["count"] = count
    question = survey.questions[count].question
    choices = survey.questions[count].choices
    return render_template("question.html", question = question, choices = choices)

@app.post('/answer')
def get_answer():
    """ Store question answer in SURVEY_ANSWERS and go to next question page
    If last question was answered, go to completion page"""

    survey_answer = request.form["answer"]
    SURVEY_ANSWERS.append(survey_answer)

    next_page = len(SURVEY_ANSWERS)
    # next_page = session["count"]+1

    if next_page == len(survey.questions):
        return redirect('/completion')

    return redirect(f'/questions/{next_page}')

@app.get('/completion')
def show_completion():
    return render_template("completion.html")
