from os import path
from flask import Flask, request, jsonify
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from dbcleanup.db_cleanup import DBCleanup


db = SQLAlchemy()
DB_NAME = "database.db"

class DBCleaner(Resource):
    def delete(self):
        key = request.headers['RegKeyDelete']

        cleanup_obj = DBCleanup(key)

        if False == cleanup_obj.validate_key():
            return jsonify({'error' : 'Use correct Reg Key to delete'})
            
        return jsonify(cleanup_obj.initiate_db_cleanup())

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dsfuibskdbvibsidbvbb" # change before deployment
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)  

    api = Api(app)
    api.add_resource(DBCleaner, '/adminDeleteDB')
    
    from .views import views
    from .auth import auth
    from .modify import modify
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(modify, url_prefix='/')
    
    from .models import UserDB
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return UserDB.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created a New Database!")