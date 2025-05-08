"""
    This is the __init__.py file that initializes the Flask application.
"""
from flask import Flask, Blueprint
from flask import Flask
from flask_jwt_extended import JWTManager
import os
from flask_login import LoginManager,login_user, logout_user, current_user, login_required
from config import Config
from .user_auth.user_class import User

def create_app():
    """
    Creates and configures the Flask application instance.

    - Loads configuration settings from the Config object.
    - Imports route modules to register application routes.

    Returns:
        Flask app: The configured Flask application object.
    """

    app = Flask(__name__)
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'images', 'profiles')

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists
    # Secret key for signing JWTs
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Change this in production

    # Set token location: can be 'headers', 'cookies', 'query_string', etc.
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    # Optional: Name of the header
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'

    jwt = JWTManager(app)
    from app.main import main
    from app.user_auth import user_auth
    from app.API import api
    from app.admin import admin
    from app.appoint import appoint
    from app.report import report_bp

    app.config.from_object(Config)
    

    login_manager = LoginManager()
    
    login_manager.login_view = 'user_auth.login'

    @login_manager.user_loader
    def load_user(user_id,remember=True):
        user = User.get_user_by_id(user_id)
        return user
    
    login_manager.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(user_auth,url_prefix='/user')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(appoint, url_prefix='/appointment')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(report_bp, url_prefix='/report')

    return app
