import os
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_login import login_required
from app.extensions import db, migrate, login_manager


def create_app():
    load_dotenv()

    app = Flask(__name__)

    # Load config
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

    # Import models (VERY IMPORTANT)
    from app.models import User, Subscription

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes.auth import auth
    from app.routes.subscription import subscription

    app.register_blueprint(auth)
    app.register_blueprint(subscription)

    # Routes
    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html")

    return app
