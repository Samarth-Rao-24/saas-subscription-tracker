from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.email_service import send_due_soon_email_for_user

test_email = Blueprint("test_email", __name__)


@test_email.route("/test-email")
@login_required
def test_email_route():
    send_due_soon_email_for_user(current_user)
    flash("Test email triggered (if any subscriptions are due).", "success")
    return redirect(url_for("dashboard"))