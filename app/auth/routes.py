from flask import render_template, redirect, url_for, flash
from app.auth import bp
from app.models import User
from app.auth.forms import LoginForm
from flask_login import login_user, logout_user

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        flash("Successfully logged in!")
        return redirect(url_for("main.index"))
    return render_template("auth/login.html", title="Log In", form=form)

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
