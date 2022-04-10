from .user import get_user, save_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, redirect, request, flash, url_for
from logger import Logger
from .constants import auth_constants

auth = Blueprint("auth", __name__)
logger = Logger()


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        _id = request.form.get("_id")
        password = request.form.get("password")

        if "@" in _id:
            user = get_user(email=_id)
        else:
            user = get_user(username=_id)

        if user and check_password_hash(user.password, password):
            flash("Logged in successfully!", category="success")
            login_user(user, remember=True)
            return redirect(url_for("views.home"))
        else:
            flash("Incorrect username or password.", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        full_name = request.form.get("full_name")
        gender = request.form.get("gender")
        occupation = request.form.get("occupation", "None")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_username = get_user(username=username)
        user_email = get_user(email=email)

        if user_username:
            flash("Username already exists.", category="error")
        elif user_email:
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(full_name) < 2:
            flash("First Name must be greater than 1 characters.", category="error")
        elif not gender:
            flash("Please specify your gender", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password2) <= 3:
            flash("Password must be greater than 3 characters.", category="error")
        else:
            save_user(
                username=username,
                email=email,
                full_name=full_name,
                password=generate_password_hash(password1),
                gender=gender,
                occupation=occupation
            )

            login_user(get_user(username=username), remember=True)
            flash("Account created!", category="success")

            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)
