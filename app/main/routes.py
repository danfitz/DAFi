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
        masterGoal = Goal(goal=form.masterGoal.data, user=current_user)
        masterGoal.makeMaster()

        # Saves master goal to database
        db.session.add(masterGoal)
        db.session.commit()

        # Finally, redirect to next prompt, the breakdown of the master goal
        return redirect(url_for("main.master_breakdown"))

    return render_template("new-master.html", form=form)

@bp.route("/master-breakdown", methods=["GET", "POST"])
@login_required
def master_breakdown():
    # Grab newest master goal added to user's goals
    masterGoal = Goal.query.filter(Goal.user==current_user, Goal.is_master==True).order_by(Goal.id.desc()).first()
    form = ChildGoalsForm()

    if form.validate_on_submit():
        # Grab child goals from form data
        childGoals = form.childGoals.data.split("\r\n")

        for i in range(len(childGoals)):
            if i == 0:
                # If it's the first child goal, make it the child of the master goal (happens only once)
                g = Goal(goal=childGoals[i], user=current_user)
                masterGoal.addChild(g)
                db.session.add(masterGoal)
                db.session.add(g)
                db.session.commit()
            else:
                # Otherwise, make the child goal a child of the goal before it
                g = Goal.query.filter_by(goal=childGoals[i-1]).first()
                g2 = Goal(goal=childGoals[i], user=current_user)
                g.addChild(g2)
                db.session.add(g)
                db.session.add(g2)
                db.session.commit()

        return redirect(url_for("main.tree", masterGoal=masterGoal.goal))

    return render_template("master-breakdown.html", masterGoal=masterGoal, form=form)

@bp.route("/tree/<masterGoal>")
@login_required
def tree(masterGoal):
    masterGoal = Goal.query.filter_by(goal=masterGoal).first()

    # Redirects back to homepage if goal passed in URL isn't a master goal (i.e., goal has parents)
    if masterGoal.parents.all() != []:
        return redirect(url_for("main.index"))

    # Create empty array
    treeList = []

    # Append master goal
    treeList.append(masterGoal)

    # Append first child of master goal
    childGoal = masterGoal.children[0]
    treeList.append(childGoal)

    # Append children of children until no children remain
    while childGoal.children.all() != []:
        for child in childGoal.children:
            treeList.append(child)
        childGoal = childGoal.children[0]

    treeList2 = Goal.listTree(masterGoal, [])

    return render_template("tree.html", treeList=treeList, treeList2=treeList2)
