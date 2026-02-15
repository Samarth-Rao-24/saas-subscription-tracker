from app.extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"   # Explicit table name

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    subscriptions = db.relationship(
        'Subscription',
        backref='owner',
        lazy=True
    )