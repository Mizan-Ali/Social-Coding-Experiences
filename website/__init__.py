from flask import Flask, request, jsonify
from logger import Logger
from .models import mongo
from .user import get_user
from flask_login import LoginManager
from flask_restful import Resource, Api
from .constants import init_constants
from apscheduler.schedulers.background import BackgroundScheduler
from dbcleanup.db_cleanup import DBCleanup

def create_app():
    function = 'create_app'
    print('DEBUG', function, 'Initiating app creation')
    app = Flask(__name__)

    app.config["SECRET_KEY"] = init_constants['APP_CONFIG_SECRET_KEY']
    app.config["MONGO_URI"] = init_constants['MONGO_URI']
    print('DEBUG', function, 'App created successfully')

    print('DEBUG', function, 'Connecting to DB')
    mongo.init_app(app)
    logger = Logger(mongo)
    logger.debug(0, function, 'Connection to DB successful')

    class DBCleaner(Resource):
        def delete(self):
            key = request.headers["RegKeyDelete"]
            cleanup_obj = DBCleanup(key, mongo)

            if False == cleanup_obj.validate_key():
                return jsonify({'error': init_constants['WRONG_DELETE_REGKEY']})
            
            resp = cleanup_obj.initiate_db_cleanup(mongo)

            return jsonify(resp)

        def get(self):
            return jsonify({'Logging Level': logger.get_debug_lvl()})
        
        def put(self):
            function = 'AdminOperations.PUT'
            dbglvl = request.headers['DEBUGLVL']
            logger.debug(0, function, f'Setting DEBUG Level from [{logger.get_debug_lvl()}] to [{dbglvl}]')
            logger.set_debug_lvl(dbglvl)

            return jsonify({'New Debug Level': dbglvl})

    
    api = Api(app)
    api.add_resource(DBCleaner, "/adminOperations")

    from .auth import auth
    from .views import views
    from .modify import modify

    logger.debug(0, function, 'Registering auth blueprint')
    app.register_blueprint(auth, url_prefix="/")
    logger.debug(0, function, 'Registring views blueprint')
    app.register_blueprint(views, url_prefix="/")
    logger.debug(0, function, 'Registring modify blueprint')
    app.register_blueprint(modify, url_prefix="/")

    logger.debug(0, function, 'Initiating login manager')
    login_manager = LoginManager()
    login_manager.login_view = "views.home"
    login_manager.init_app(app)
    logger.debug(0, function, 'Login manager initiated')

    try:
        import logging
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)
        rating_updater = BackgroundScheduler(daemon = True)
        rating_updater.add_job(update_all_ratings, 'interval', hours=10)
        rating_updater.start()
        logger.scheduler(rating_updater)
    except Exception as e:
        logger.error(0, function, f'Error while scheduling leaderboard refresh : {e}')

    @login_manager.user_loader
    def load_user(username):
        return get_user(username)

    return app


def update_all_ratings():
    function = 'update_all_ratings'
    l_user_data = {}
    try:
        users_collection = mongo.db.users
        for user_data in users_collection.find({}):
            user = get_user(user_data['_id'])
            user.update_rating()
            l_user_data = user_data

    except Exception as e:
        print('ERROR', function, f'Error while updating ratings for all users : {e}', **l_user_data)