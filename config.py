import os
from dotenv import load_dotenv

load_dotenv(".env.local")
# პოულობს იმ საქაღალდის გზას, სადაც ეს ფაილი დევს
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env.local"))   

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") or "fallback-dev-key-change-in-prod"
    
    # Flask-Mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_RECEIVER = os.environ.get("MAIL_RECEIVER")
    
    # Security headers
    SESSION_COOKIE_SECURE = False   # Set True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    WTF_CSRF_ENABLED = True


class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
