from logger import Logger
from .user import get_user, save_user
from .constants import auth_constants
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, redirect, request, flash, url_for, session
from .models import mongo

logger = Logger(mongo)
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    function = "auth.login"
    if request.method == "POST":
        _id = request.form.get("_id")
        password = request.form.get("password")
        logger.debug(
            0, function, "Recieved login request", **{"Login request recived from": _id}
        )

        if "@" in _id:
            logger.debug(0, function, "Email ID recieved as login parameter")
            user = get_user(email=_id)
        else:
            logger.debug(0, function, "User name received as login parameter")
            user = get_user(username=_id)

        if user and check_password_hash(user.password, password):
            logger.debug(0, function, f"User [{_id}] authenticated")
            flash("Logged in successfully!", category="success")
            login_user(user, remember=True)
            logger.debug(0, function, f"Saving login data for user [{_id}]")
            return redirect(url_for("views.profile"))
        else:
            logger.error(0, function, f"Error in authenticating user [{_id}]")
            if user:
                logger.error(
                    0, function, f"Password provided for user [{_id}] is wrong"
                )
            else:
                logger.error(
                    0, function, f"User [{_id}] does not exist in the database"
                )
            flash("Incorrect username or password.", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    function = "auth.logout"
    username = ""

    if "_user_id" in session:
        username = session["_user_id"]

    logger.debug(0, function, f"User [{username}] logged out successfully")
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    function = "auth.signup"
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        full_name = request.form.get("full_name")
        gender = request.form.get("gender")
        occupation = request.form.get("occupation", "None")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        signup_dump = {
            "username": username,
            "email": email,
            "full_name": full_name,
            "gender": gender,
            "occupation": occupation,
        }
        logger.debug(
            0,
            function,
            f"Received Sign-Up request for user [{username}]",
            **signup_dump,
        )

        user_username = get_user(username=username)
        user_email = get_user(email=email)

        if user_username:
            logger.error(
                0, function, f"Cannot add new user. User [{username}] already exists"
            )
            flash("Username already exists.", category="error")
        elif user_email:
            logger.error(
                0, function, f"Cannot add new user. Email [{email}] already exists"
            )
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            logger.error(
                0,
                function,
                f"Cannot create account for user [{username}]. Email must be greater than 3 characters.",
            )
            flash("Email must be greater than 3 characters.", category="error")
        elif len(full_name) < 2:
            logger.error(
                0,
                function,
                f"Cannot create account for user [{username}]. Name length is not valid",
            )
            flash("First Name must be greater than 1 characters.", category="error")
        elif not gender:
            logger.error(
                0,
                function,
                f"Cannot create account for user [{username}]. Gender not specified",
            )
            flash("Please specify your gender", category="error")
        elif password1 != password2:
            logger.error(
                0,
                function,
                f"Cannot create account for user [{username}]. Password and confirm pasword do not match.",
            )
            flash("Passwords don't match.", category="error")
        elif len(password2) <= 3:
            logger.error(
                0,
                function,
                f"Cannot create account for user [{username}]. Password length is less than 3 characters.",
            )
            flash("Password must be greater than 3 characters.", category="error")
        else:
            logger.debug(
                0, function, f"Creating account for user [{username}].", **signup_dump
            )
            save_user(
                username=username,
                email=email,
                full_name=full_name,
                password=generate_password_hash(password1),
                gender=gender,
                occupation=occupation,
            )

            logger.debug(0, function, f"User account created for user [{username}]")
            logger.debug(0, function, f"Logging in user [{username}]")
            login_user(get_user(username=username), remember=True)
            flash("Account created!", category="success")

            return redirect(url_for("views.profile"))

    return render_template("signup.html", user=current_user)
