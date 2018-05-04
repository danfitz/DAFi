from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, TextAreaField
from wtforms.validators import DataRequired

class MasterGoalForm(FlaskForm):
    masterGoal = StringField("What's your goal?", validators=[DataRequired()])
    submit = SubmitField("Let's start")

class ChildGoalsForm(FlaskForm):
    childGoals = TextAreaField("Goal Breakdown", validators=[DataRequired()])
    # childGoals = FieldList(StringField("Is this your smallest goal?", validators=[DataRequired()]), min_entries=1, max_entries=50)
    submit = SubmitField("Continue")
