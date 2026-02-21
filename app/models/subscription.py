from datetime import datetime
from app.extensions import db


class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    billing_date = db.Column(db.Date, nullable=False)

    category = db.Column(db.String(100), nullable=False, default="General")
    frequency = db.Column(db.String(20), nullable=False, default="Monthly")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )