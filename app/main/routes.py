from app import db
from flask import render_template, redirect, current_app, url_for, request
from app.main import bp
from app.models import User, Goal
from app.main.forms import MasterGoalForm, ChildGoalsForm
from flask_login import login_required, current_user

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
def new_master():
    form = MasterGoalForm()

    if form.validate_on_submit():
        # Creates new master goal
        master_goal = Goal(goal=form.master_goal.data, user=current_user)
        master_goal.make_master()

        # Saves master goal to database
        db.session.add(master_goal)
        db.session.commit()

        # Finally, redirect to next prompt, the breakdown of the master goal
        return redirect(url_for("main.master_breakdown"))

    return render_template("new-master.html", form=form)

@bp.route("/master-breakdown", methods=["GET", "POST"])
@login_required
def master_breakdown():
    # grab newest master goal added to user's goals
    master_goal = Goal.query.filter(Goal.user==current_user, Goal.is_master==True).order_by(Goal.id.desc()).first()
    form = ChildGoalsForm()

    if form.validate_on_submit():
        # Add each goal one after the other, making the first into the child of the master, the next the child of the second, etc.
        childGoals = form.childGoals.data.split("\r\n")

        for i in range(len(childGoals)):
            g = Goal(goal=childGoals[i], user=current_user)
            if i == 0:
                master_goal.add_child(g)
                db.session.add(master_goal)
                db.session.add(g)
                db.session.commit()
            else:
                g2 = Goal.query.filter_by(goal=childGoals[i-1]).first()
                g.add_child(g2)
                db.session.add(g)
                db.session.add(g2)
                db.session.commit()

        return str(goals)
    return render_template("master-breakdown.html", master_goal=master_goal, form=form)

@bp.route("/tree/<master_goal>")
@login_required
def tree(master_goal):
    return render_template("tree.html")
