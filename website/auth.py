from . import db
from .models import UserDB
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, redirect, request, flash, url_for


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = UserDB.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash("Logged in successfully!", category="success")
            login_user(user, remember=True) 
            return redirect(url_for("views.home"))
        else:
            flash("Incorrect email or password.", category="error")
        
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        full_name = request.form.get("full_name")
        gender = request.form.get("gender")
        occupation = request.form.get("occupation", "None")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user = UserDB.query.filter_by(email=email).first()
        if user:
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
            new_user = UserDB(
                email=email, 
                full_name=full_name, 
                gender=gender,
                occupation=str(occupation),
                password=generate_password_hash(password=password1, method="sha256")
                )
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user, remember=True)
            flash("Account created!", category="success")

            return redirect(url_for("views.home"))
            
    return render_template("signup.html", user=current_user)
