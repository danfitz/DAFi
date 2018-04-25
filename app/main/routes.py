from app import db
from flask import render_template, redirect, current_app
from app.main import bp
from app.main.forms import MasterGoalForm, ChildGoalsForm
from flask_login import login_required

import os
from flask import send_from_directory

# view function necessary for favicon to appear
@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@bp.route("/")
@login_required
def index():
    return render_template("index.html")

@bp.route("/new-master", methods=["GET", "POST"])
@login_required
def master_goal():
    form = MasterGoalForm()
    if form.validate_on_submit():
        pass
        # Add master goal to current user
        # return redirect("new-tree.html")
    return render_template("new-master.html", form=form)

@bp.route("/new-tree", methods=["GET", "POST"])
@login_required
def new_tree():
    # master_goal = filter for newest master goal added to db
    form = ChildGoalsForm()
    if form.validate_on_submit():
        return str(form.childGoals.data)
    return render_template("new-tree.html", form=form)
