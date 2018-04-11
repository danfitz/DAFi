from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList
from wtforms.validators import DataRequired

class MasterGoalForm(FlaskForm):
    master_goal = StringField("What's your goal?", validators=[DataRequired()])
    submit = SubmitField("Let's start")

class ChildrenForm(FlaskForm):
    children = FieldList(StringField("Is this your smallest goal?", validators=[DataRequired()], min_entries=3, max_entries=50))
