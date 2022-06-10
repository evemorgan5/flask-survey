from urllib import response
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# SURVEY_ANSWERS = []

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get('/')
def display_survey():
    """ Load homepage with survey title, instructions, and survey start button """
    return render_template("survey_start.html", survey=survey)

@app.post("/begin")
def begin_responses():
    session["responses"] = []
    return redirect("/questions/0")


@app.get('/questions/<int:count>')
def show_questions(count):
    """ Display question with answer choices as radio buttons
    If page number is not equal to the length of responses,
    redirect to the correct page and return flash message """
    if count != len(session["responses"]):
        flash("Trying to access an invalid question!")
        return redirect(f'/questions/{len(session["responses"])}')
    if len(survey.questions) == len(session["responses"]):
        return redirect('/completion')

    question = survey.questions[count].question
    choices = survey.questions[count].choices
    return render_template("question.html", question = question, choices = choices)

@app.post('/answer')
def get_answer():
    """ Store question answer in session variable and go to next question page
    If last question was answered, go to completion page"""

    survey_answer = request.form["answer"]

    survey_responses = session["responses"]
    survey_responses.append(survey_answer)
    session["responses"] = survey_responses

    next_page = len(session["responses"])

    if next_page == len(survey.questions):
        return redirect('/completion')

    return redirect(f'/questions/{next_page}')


@app.get('/completion')
def show_completion():
    """ Display completion page """
    # print(session["responses"])
    # breakpoint()

    return render_template("completion.html")

