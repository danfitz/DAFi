from app.main import bp
from flask import render_template, current_app
from flask_login import login_required

import os
from flask import send_from_directory

@bp.route("/")
@login_required
def index():
    return render_template("index.html")

# view function necessary for favicon to appear
@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')
