import json
from app import db
from flask import render_template, redirect, current_app, url_for, request, jsonify
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
    masterGoals = Goal.query.filter_by(is_master=True)

    return render_template("index.html", masterGoals=masterGoals)

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

@bp.route("/tree/<masterGoal>", methods=["GET", "POST"])
@login_required
def tree(masterGoal):

    if request.method == "GET":
        masterGoal = Goal.query.filter_by(goal=masterGoal).first()

        # Redirects back to homepage if goal passed in URL doesn't exist
        # OR goal isn't a master goal
        if not masterGoal or masterGoal.is_master == False:
            return redirect(url_for("main.index"))

        # Creates jsonTree
        jsonTree = Goal.jsonTree(masterGoal)

        # Function that returns an HTML-rendered version of jsonTree, optimized for jsTree
        def jsonTreeToHtml(jsonTree):
            goal = Goal.query.get(jsonTree["id"])
            if goal.is_master == True:
                html = "<ul><li data-goal-id=%s data-jstree='{\"selected\": true, \"opened\": true}'>%s" % (jsonTree["id"], jsonTree["text"])
            else:
                html = "<ul><li data-goal-id=%s data-jstree='{\"opened\": true}'>%s" % (jsonTree["id"], jsonTree["text"])

            if jsonTree["children"]:
                for childGoalJson in jsonTree["children"]:
                    html += jsonTreeToHtml(childGoalJson)

            html += "</ul>"
            return html

        treeHtml = jsonTreeToHtml(jsonTree)

        return render_template("tree.html", jsonTree=jsonTree, treeHtml=treeHtml)


    elif request.method == "POST":
        # Obtains JSON in jsTree from POST request sent in tree.html and converts it to JSON object
        jsonTree = json.loads(request.form["json"])

        def saveTree(jsonTree, masterFound=False):
            # Grabs Goal object from id in JSON
            goal = Goal.query.get(int(jsonTree["id"]))

            # Makes first goal in JSON into master and all others NOT into master
            if masterFound == False:
                goal.is_master = True
            else:
                goal.is_master = False

            # Removes all child goal relationships
            if goal.children.all() != []:
                for childGoal in goal.children.all():
                    goal.removeRel(childGoal)

            # Adds new relationships if goal has children
            if jsonTree["children"]:
                for childGoalJson in jsonTree["children"]:
                    childGoal = Goal.query.get(int(childGoalJson["id"]))
                    goal.addChild(childGoal)
                    saveTree(childGoalJson, masterFound=True)

            # Finally, add goal to db session
            db.session.add(goal)

        saveTree(jsonTree)
        db.session.commit()

        masterGoal = Goal.query.get(int(jsonTree["id"]))

        return redirect(url_for("main.tree", masterGoal=masterGoal.goal))
