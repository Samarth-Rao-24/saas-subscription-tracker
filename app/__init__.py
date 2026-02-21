import os
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_login import login_required, current_user
from app.extensions import db, migrate, login_manager, mail
from datetime import datetime, date, timedelta
from collections import defaultdict
from flask_mail import Message


def create_app():
    load_dotenv()

    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object("app.config.ProductionConfig")
    else:
        app.config.from_object("app.config.DevelopmentConfig")

    # --------------------
    # Initialize extensions
    # --------------------
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = "auth.login"

    # --------------------
    # Models
    # --------------------
    from app.models.user import User
    from app.models.subscription import Subscription

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # --------------------
    # EMAIL: Upcoming renewals (FIXED)
    # --------------------
    def send_upcoming_renewals_email(user):
        today = date.today()
        limit = today + timedelta(days=7)

        upcoming = []

        for sub in user.subscriptions:
            next_billing = calculate_next_billing(sub)
            days_left = (next_billing - today).days

            if 0 <= days_left <= 7:
                upcoming.append((sub, next_billing, days_left))

        if not upcoming:
            return False

        body = f"Hi {user.name},\n\n"
        body += "You have the following subscriptions due soon:\n\n"

        for sub, billing_date, days_left in upcoming:
            body += (
                f"• {sub.name}\n"
                f"  Amount: ₹{sub.price}\n"
                f"  Due Date: {billing_date.strftime('%d %b %Y')} "
                f"({days_left} days left)\n\n"
            )

        body += "Please make sure your payment method is up to date.\n\n— SaaS Tracker"

        msg = Message(
            subject="⏰ Upcoming Subscription Payments",
            recipients=[user.email],
            body=body
        )

        mail.send(msg)
        return True

    # --------------------
    # Blueprints
    # --------------------
    from app.routes.auth import auth
    from app.routes.subscription import subscription
    from app.routes.test_email import test_email

    app.register_blueprint(auth)
    app.register_blueprint(subscription)
    app.register_blueprint(test_email)

    # --------------------
    # Routes
    # --------------------
    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/dashboard")
    @login_required
    def dashboard():
        subscriptions = current_user.subscriptions
        today = date.today()

        for sub in subscriptions:
            next_billing = calculate_next_billing(sub)
            sub.next_billing = next_billing

            days_remaining = (next_billing - today).days
            sub.days_remaining = days_remaining

            if days_remaining < 0:
                sub.status = "Overdue"
            elif days_remaining <= 7:
                sub.status = "Due Soon"
            else:
                sub.status = "Active"

        total_monthly = 0
        yearly_total = 0

        for sub in subscriptions:
            if sub.frequency == "Monthly":
                total_monthly += sub.price
                yearly_total += sub.price * 12
            elif sub.frequency == "Yearly":
                total_monthly += sub.price / 12
                yearly_total += sub.price

        upcoming = [sub for sub in subscriptions if 0 <= sub.days_remaining <= 7]

        category_totals = defaultdict(float)
        for sub in subscriptions:
            category_totals[sub.category] += sub.price

        category_labels = list(category_totals.keys())
        category_values = list(category_totals.values())

        monthly_totals = defaultdict(float)
        for sub in subscriptions:
            month = sub.billing_date.strftime("%Y-%m")
            monthly_totals[month] += sub.price

        monthly_labels = sorted(monthly_totals.keys())
        monthly_values = [monthly_totals[m] for m in monthly_labels]

        return render_template(
            "dashboard.html",
            subscriptions=subscriptions,
            total_monthly=total_monthly,
            yearly_total=yearly_total,
            upcoming=upcoming,
            category_labels=category_labels,
            category_values=category_values,
            monthly_labels=monthly_labels,
            monthly_values=monthly_values,
        )

    # expose email helper for test_email blueprint
    app.send_upcoming_renewals_email = send_upcoming_renewals_email

    return app


# --------------------
# Billing Date Calculator
# --------------------
def calculate_next_billing(sub):
    today = date.today()
    billing_date = sub.billing_date

    if sub.frequency == "Monthly":
        while billing_date <= today:
            month = billing_date.month + 1
            year = billing_date.year
            if month > 12:
                month = 1
                year += 1
            billing_date = billing_date.replace(year=year, month=month)

    elif sub.frequency == "Yearly":
        while billing_date <= today:
            billing_date = billing_date.replace(year=billing_date.year + 1)

    return billing_date