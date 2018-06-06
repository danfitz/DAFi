import json
from app import db
from flask import render_template, redirect, current_app, url_for, request, jsonify
from app.main import bp
from app.models import User, Goal
from app.main.forms import MasterGoalForm, ChildGoalsForm
from flask_login import login_required, current_user

import os
from flask import send_from_directory

# VIEW FUNCTION: necessary for favicon to appear
@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')


# VIEW FUNCTION: homepage
@bp.route("/")
@login_required
def index():
    masterGoals = Goal.query.filter_by(is_master=True)

    return render_template("index.html", masterGoals=masterGoals)


# VIEW FUNCTION: step 1 of new goal tree - master goal form
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
        return redirect(url_for("main.master_breakdown", masterGoalId=masterGoal.id))

    return render_template("new-master.html", form=form)


# VIEW FUNCTION: step 2 of new goal tree - master goal breakdown
@bp.route("/master-breakdown/<masterGoalId>", methods=["GET", "POST"])
@login_required
def master_breakdown(masterGoalId):
    # Grab master goal added to user's goals in step 1 (previous view function)
    masterGoal = Goal.query.get(masterGoalId)
    form = ChildGoalsForm()

    if form.validate_on_submit():
        # Grab child goals from form data
        childGoals = form.childGoals.data.split("\r\n")

        for i in range(len(childGoals)):
            if i == 0:
                # If it's the first child goal, make it the child of the master goal (happens only once)
                childGoal = Goal(goal=childGoals[i], user=current_user)
                masterGoal.addChild(childGoal)
                db.session.add(masterGoal)
                db.session.add(childGoal)
                db.session.commit()
            else:
                # Otherwise, make the child goal a child of the goal before it
                goal = Goal.query.filter_by(goal=childGoals[i-1]).first()
                childGoal = Goal(goal=childGoals[i], user=current_user)
                goal.addChild(childGoal)
                db.session.add(goal)
                db.session.add(childGoal)
                db.session.commit()

        return redirect(url_for("main.tree", masterGoalId=masterGoal.id))

    return render_template("master-breakdown.html", masterGoal=masterGoal, form=form)


# VIEW FUNCTION: single goal tree view
@bp.route("/tree/<masterGoalId>", methods=["GET", "POST"])
@login_required
def tree(masterGoalId):

    ### CREATES TREE VIEW ###
    if request.method == "GET":
        masterGoal = Goal.query.get(masterGoalId)

        # Redirects back to homepage if goal passed in URL doesn't exist
        # OR goal isn't a master goal
        if not masterGoal or masterGoal.is_master == False:
            return redirect(url_for("main.index"))

        # Creates jsonTree
        jsonTree = Goal.jsonTree(masterGoal)

        return render_template("tree.html", jsonTree=jsonTree)

    ### SAVES TREE VIEW IN DATABASE ###
    elif request.method == "POST":
        # Obtains JSON string in jsTree from POST request (code in tree.html) and converts it to JSON object
        jsonTree = json.loads(request.form["json"])

        def saveTree(jsonTree, masterFound=False):
            # Grabs Goal object from id in JSON if id is real
            # Otherwise, creates Goal object if goal doesn't already exist
            try:
                int(jsonTree["id"])
                goal = Goal.query.get(jsonTree["id"])
            except ValueError:
                goal = Goal(goal=jsonTree["text"])
                db.session.add(goal)
                db.session.commit()
                # Replaces id with database id rather than pre-placed id given by jsTree
                jsonTree["id"] = goal.id

            # Renames goal in database if it was changed in tree
            if goal.goal != jsonTree["text"]:
                goal.goal = jsonTree["text"]
                db.session.add(goal)
                db.session.commit()

            # Makes first goal in JSON into master and all others NOT into master
            if masterFound == False:
                goal.is_master = True
            else:
                goal.is_master = False

            # Removes all child goal relationships
            if goal.children.all() != []:
                for childGoal in goal.children.all():
                    goal.removeRel(childGoal)

                    # Removes goal (and all its children) from database if goal isn't in jsonTree
                    def goalInJson(goal, jsonTree):
                        for childGoalJson in jsonTree["children"]:
                            if goal.goal == childGoalJson["text"]:
                                return True
                            goalInJsonCheck(goal, childGoalJson)
                        return False

                    def removeChildren(goal):
                        childGoals = goal.children.all()
                        if childGoals != []:
                            for childGoal in childGoals:
                                removeChildren(childGoal)
                        db.session.delete(goal)

                    if goalInJson(childGoal, jsonTree):
                        removeChildren(childGoal)
                        db.session.commit()

            # Adds new relationships if goal's JSON has children
            if jsonTree["children"]:
                for childGoalJson in jsonTree["children"]:
                    # Grabs childGoal object from id in JSON if id is real
                    # Otherwise, creates childGoal object if childGoal doesn't already exist
                    try:
                        int(childGoalJson["id"])
                        childGoal = Goal.query.get(childGoalJson["id"])
                    except ValueError:
                        childGoal = Goal(goal=childGoalJson["text"])
                        db.session.add(childGoal)
                        db.session.commit()
                        # Replaces id with database id rather than pre-placed id given by jsTree
                        childGoalJson["id"] = childGoal.id
                    # Makes childGoal a child of goal
                    goal.addChild(childGoal)
                    # Recursively loops through children of children of children
                    saveTree(childGoalJson, masterFound=True)

            # Finally, add goal to database
            db.session.add(goal)
            db.session.commit()

        saveTree(jsonTree)

        masterGoal = Goal.query.get(int(jsonTree["id"]))

        return redirect(url_for("main.tree", masterGoalId=masterGoal.id))
