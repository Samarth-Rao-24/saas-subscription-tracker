import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
