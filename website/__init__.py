import os
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask import Flask, request, jsonify
from dbcleanup.db_cleanup import DBCleanup


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    # change before deployment
    app.config["SECRET_KEY"] = "dsfuibskdbvibsidbvbb"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    class DBCleaner(Resource):
        def delete(self):
            key = request.headers["RegKeyDelete"]

            cleanup_obj = DBCleanup(key)

            if False == cleanup_obj.validate_key():
                return jsonify({"error": "Use correct Reg Key to delete"})

            resp = cleanup_obj.initiate_db_cleanup()

            if resp.get("cleanup_status", "FAILURE") == "SUCCESS":
                print("LOGGER: Creating Db after cleanup")
                create_database(app)

            return jsonify(resp)

    api = Api(app)
    api.add_resource(DBCleaner, "/adminDeleteDB")

    from .views import views
    from .auth import auth
    from .modify import modify

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(modify, url_prefix="/")

    from .models import User

    try:
        create_database(app)

    except Exception as e:
        print("LOGGER: Cannot create new Db. Restart the app")
        print(f"ERROR: {e}")

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    cwd = os.path.abspath(os.curdir)
    path_to_db = cwd + "/website/"

    print(f"LOGGER: Db path: {cwd}")
    print(f"LOGGER: Database exists [{os.path.exists(path_to_db + DB_NAME)}]")
    if not os.path.exists(path_to_db + DB_NAME):
        db.create_all(app=app)
        print("LOGGER: Created a New Database!")
