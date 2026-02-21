from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.email_service import send_due_soon_email_for_user

test_email = Blueprint("test_email", __name__)


@test_email.route("/test-email")
@login_required
def test_email_route():
    try:
        sent = send_due_soon_email_for_user(current_user)

        if sent:
            flash("Test email sent successfully.", "success")
        else:
            flash("No subscriptions due in the next 7 days.", "info")

    except Exception as e:
        print("TEST EMAIL ERROR:", e)
        flash("Failed to send test email.", "danger")

    return redirect(url_for("dashboard"))