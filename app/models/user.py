from flask_login import UserMixin
from app.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    subscriptions = db.relationship(
        "Subscription",
        backref="user",              # ✅ sub.user
        lazy=True,
        cascade="all, delete-orphan"
    )