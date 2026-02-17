import os
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_login import login_required, current_user
from app.extensions import db, migrate, login_manager
from datetime import datetime, timedelta
from collections import defaultdict


def create_app():
    load_dotenv()

    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object("app.config.ProductionConfig")
    else:
        app.config.from_object("app.config.DevelopmentConfig")

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.models import User, Subscription

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth
    from app.routes.subscription import subscription

    app.register_blueprint(auth)
    app.register_blueprint(subscription)

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/dashboard")
    @login_required
    def dashboard():

        subscriptions = current_user.subscriptions

        total = sum(sub.price for sub in subscriptions)

        today = datetime.now().date()
        next_7_days = today + timedelta(days=7)

        upcoming = [
            sub for sub in subscriptions
            if today <= sub.billing_date <= next_7_days
        ]

        yearly_total = total * 12

        category_totals = defaultdict(float)

        for sub in subscriptions:
            category_totals[sub.category] += sub.price

        category_labels = list(category_totals.keys())
        category_values = list(category_totals.values())

        return render_template(
            "dashboard.html",
            subscriptions=subscriptions,
            total=total,
            yearly_total=yearly_total,
            upcoming=upcoming,
            category_labels=category_labels,
            category_values=category_values
        )

    return app
