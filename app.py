from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "survey"
RESPONSES_KEY = "responses"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route("/session", methods=["POST"])
def session():
    session[RESPONSES_KEY] = []
    return redirect("/")

@app.route("/")
def cover_page():
    this_title = satisfaction_survey.title
    these_instructions = satisfaction_survey.instructions
    return render_template("base.html", this_title=this_title, these_instructions=these_instructions)

@app.route("/questions/<int:qid>")
def survey_page(qid):
    if (responses is None):
        # trying to access question page too soon
        return redirect("/")
    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")
    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    question = satisfaction_survey.questions[qid].question
    choices = satisfaction_survey.questions[qid].choices
    return render_template("survey.html", question=question, choices=choices)


# @app.route("/questions/0")
# def survey_page_0():
    # question= satisfaction_survey.questions[0].question
    # choices_0  = satisfaction_survey.questions[0].choices
    # return render_template("survey.html", question_0=question_0, choices_0=choices_0)
# 
@app.route("/answers", methods=["POST"])
def answers():
    choice = request.form['answer']
    responses =session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    return redirect(f"/questions/{len(responses)}")

@app.route("/complete")
def complete():
    return render_template("complete.html", responses=responses)


# This code was written Before understanding how to incorporate an increasing integer in the route:
#  
# @app.route("/questions/2")
# def survey_page_2():
    # question_2 = satisfaction_survey.questions[2].question
    # return render_template("survey.html", question_2=question_2)
# 
# @app.route("/questions/3")
# def survey_page_3():
    # question_3 = satisfaction_survey.questions[3].question
    # return render_template("survey.html", question_3=question_3, responses=responses)