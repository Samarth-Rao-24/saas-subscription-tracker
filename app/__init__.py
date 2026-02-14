import os
from flask import Flask
from dotenv import load_dotenv

from app.extensions import db, migrate, login_manager


def create_app():
    load_dotenv()

    app = Flask(__name__)

    # Load environment config
    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object("app.config.ProductionConfig")
    else:
        app.config.from_object("app.config.DevelopmentConfig")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    # Import models AFTER initializing extensions
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes.auth import auth
    app.register_blueprint(auth)

    @app.route("/")
    def home():
        return "SaaS Subscription Tracker is running 🚀"

    return app
