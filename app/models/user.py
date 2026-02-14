from datetime import datetime
from app.extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__='users'

    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80), nullable=False, unique=True)
    email=db.Column(db.String(120),nullable=False, unique=True)
    password_hash=db.Column(db.String(255), nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"