from flask_mail import Message
from flask import current_app
from datetime import datetime
from app.extensions import mail


def send_due_soon_email_for_user(user):
    """
    Sends due-soon subscription email to a single user.
    Returns True if email sent, False otherwise.
    """

    today = datetime.now().date()
    due_subscriptions = []

    for sub in user.subscriptions:
        if not sub.billing_date:
            continue

        days_remaining = (sub.billing_date - today).days

        if 0 <= days_remaining <= 7:
            due_subscriptions.append(sub)

    # 🚫 Nothing due → no email
    if not due_subscriptions:
        print(f"No due subscriptions for {user.email}")
        return False

    msg = Message(
        subject="⏰ Upcoming Subscription Payments",
        recipients=[user.email],
        sender=current_app.config["MAIL_DEFAULT_SENDER"]
    )

    msg.body = (
        f"Hi {user.username},\n\n"
        "You have the following subscriptions due soon:\n\n"
    )

    for sub in due_subscriptions:
        msg.body += (
            f"• {sub.name}\n"
            f"  Amount: ₹{sub.price}\n"
            f"  Due Date: {sub.billing_date.strftime('%d %b %Y')}\n\n"
        )

    msg.body += (
        "Please make sure your payment method is up to date.\n\n"
        "— SaaS Tracker"
    )

    mail.send(msg)
    print(f"Email sent to {user.email}")
    return True