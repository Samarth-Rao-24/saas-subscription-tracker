import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 


db=SQLAlchemy()
migrate=Migrate()


def create_app():
    load_dotenv()

    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object("app.config.ProductionConfig")
    else:
        app.config.from_object("app.config.DevelopmentConfig")

    db.init_app(app)
    migrate.init_app(app,db)

    from app.models import user


    @app.route("/")
    def home():
        return "SaaS Subscription Tracker is running 🚀"

    return app
