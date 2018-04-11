from flask import render_template, current_app
from app.main import bp
from app.main.forms import ChildrenForm
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

@bp.route("/new-tree")
@login_required
def new_tree():
    form = ChildrenForm()
    return render_template("new-tree.html", form=form)
