from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


@views.route('/')
def home():
    all_info = dict()
    return render_template("home.html", user=current_user, info=all_info)
