from datetime import date
from app.models.subscription import Subscription
from app.extensions import db
from app.utils.email_service import send_due_soon_email

# Match dashboard logic
DUE_SOON_DAYS = 7


def check_and_send_reminders():
    """
    Checks all subscriptions and sends reminder emails
    for subscriptions that are due soon.
    """

    today = date.today()

    subscriptions = Subscription.query.all()

    for sub in subscriptions:
        # Safety checks
        if not sub.user or not sub.user.email:
            continue

        days_remaining = (sub.billing_date - today).days

        if 0 < days_remaining <= DUE_SOON_DAYS:
            send_due_soon_email(
                user=sub.user,
                subscription=sub,
                days_remaining=days_remaining
            )