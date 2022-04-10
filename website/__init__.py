from flask import Flask
from logger import Logger
from .models import mongo
from .user import get_user
from flask_login import LoginManager
from .constants import init_constants
from apscheduler.schedulers.background import BackgroundScheduler

logger = Logger()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = init_constants['APP_CONFIG_SECRET_KEY']
    app.config["MONGO_URI"] = init_constants['MONGO_URI']

    mongo.init_app(app)

    from .auth import auth
    from .views import views
    from .modify import modify

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(modify, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = "views.home"
    login_manager.init_app(app)

    try:
        import logging
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)
        rating_updater = BackgroundScheduler(daemon = True)
        rating_updater.add_job(update_all_ratings, 'interval', hours=10)
        rating_updater.start()
    except Exception as e:
        print(e)

    @login_manager.user_loader
    def load_user(username):
        return get_user(username)

    return app


def update_all_ratings():
    try:
        users_collection = mongo.db.users
        for user_data in users_collection.find({}):
            user = get_user(user_data['_id'])
            user.update_rating()

    except Exception as e:
        print(e)