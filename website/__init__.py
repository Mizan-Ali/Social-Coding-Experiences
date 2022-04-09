from flask import Flask
from .models import mongo
from .user import get_user
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dsfuibskdbvibsidbvbb"
    app.config["MONGO_URI"] = "mongodb+srv://admin:duh1999@cluster0.neruc.mongodb.net/DUH?retryWrites=true&w=majority"

    mongo.init_app(app)


    from .auth import auth
    from .views import views
    from .modify import modify

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(modify, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(username):
        return get_user(username)

    return app

