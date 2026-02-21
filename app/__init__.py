import os
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_login import login_required, current_user
from app.extensions import db, migrate, login_manager, mail
from datetime import datetime, timedelta
from collections import defaultdict
from apscheduler.schedulers.background import BackgroundScheduler
from app.email_service import send_due_subscription_reminders

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
    mail.init_app(app)
    login_manager.login_view = "auth.login"

    from app.models import User, Subscription

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth
    from app.routes.subscription import subscription
    from app.routes.test_email import test_email

    app.register_blueprint(auth)
    app.register_blueprint(subscription)
    app.register_blueprint(test_email)

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/dashboard")
    @login_required
    def dashboard():
        subscriptions = current_user.subscriptions
        today = datetime.now().date()

        # ----------------------------------
        # Calculate next billing + status
        # ----------------------------------
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

        # ----------------------------------
        # Monthly Total (frequency aware)
        # ----------------------------------
        total_monthly = 0
        for sub in subscriptions:
            if sub.frequency == "Monthly":
                total_monthly += sub.price
            elif sub.frequency == "Yearly":
                total_monthly += sub.price / 12

        # ----------------------------------
        # Yearly Projection
        # ----------------------------------
        yearly_total = 0
        for sub in subscriptions:
            if sub.frequency == "Monthly":
                yearly_total += sub.price * 12
            elif sub.frequency == "Yearly":
                yearly_total += sub.price

        # ----------------------------------
        # Upcoming Bills (Next 7 Days)
        # ----------------------------------
        upcoming = [
            sub for sub in subscriptions
            if 0 <= sub.days_remaining <= 7
        ]

        # ----------------------------------
        # Category Chart
        # ----------------------------------
        category_totals = defaultdict(float)
        for sub in subscriptions:
            category_totals[sub.category] += sub.price

        category_labels = list(category_totals.keys())
        category_values = list(category_totals.values())

        # ----------------------------------
        # Monthly Spending Trend
        # ----------------------------------
        monthly_totals = defaultdict(float)
        for sub in subscriptions:
            month = sub.billing_date.strftime("%Y-%m")
            monthly_totals[month] += sub.price

        monthly_labels = sorted(monthly_totals.keys())
        monthly_values = [monthly_totals[m] for m in monthly_labels]

        return render_template(
            "dashboard.html",
            subscriptions=subscriptions,
            total_monthly=total_monthly,   # ✅ FIXED VARIABLE NAME
            yearly_total=yearly_total,
            upcoming=upcoming,
            category_labels=category_labels,
            category_values=category_values,
            monthly_labels=monthly_labels,
            monthly_values=monthly_values
        )

    # ----------------------------------
    # Start Background Jobs
    # ----------------------------------
    start_scheduler(app)

    return app


# ----------------------------------
# Billing Date Calculator
# ----------------------------------
def calculate_next_billing(sub):
    today = datetime.now().date()
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

# ----------------------------------
# Background Scheduler Setup
# ----------------------------------

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=send_due_subscription_reminders,
    trigger='interval',
    days=1
)
scheduler.start()


def start_scheduler(app):
    if not scheduler.running:
        scheduler.add_job(
            func=lambda: run_with_app_context(app),
            trigger="interval",
            minutes=60,  # change later (e.g. daily)
            id="email_reminder_job",
            replace_existing=True
        )
        scheduler.start()


def run_with_app_context(app):
    with app.app_context():
        from app.utils.email_reminder import check_and_send_reminders
        check_and_send_reminders()
