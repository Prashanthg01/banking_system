from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from app.utils.error_handlers import register_error_handlers

mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        # Register Blueprints
        from app.views.auth_view import auth_bp
        from app.views.banker_view import banker_bp
        from app.views.customer_view import customer_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(banker_bp, url_prefix='/banker')
        app.register_blueprint(customer_bp, url_prefix='/customer')

        # Register error handlers
        register_error_handlers(app)

    return app
