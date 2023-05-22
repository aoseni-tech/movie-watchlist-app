from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base config."""

    SECRET_KEY = environ.get("SECRET_KEY")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"


class Dev_Config(Config):
    """Development configuration"""

    ENV = "development"
    DEBUG = True
    TESTING = False
    DATABASE_URI = environ.get("DEV_DATABASE_URI")


class Test_Config(Config):
    """Development configuration"""

    ENV = "testing"
    DEBUG = True
    TESTING = True
    DATABASE_URI = environ.get("DEV_DATABASE_URI")
    WTF_CSRF_ENABLED = False


class Prod_Config(Config):
    """Development configuration"""

    ENV = "PRODUCTION"
    DEBUG = False
    TESTING = False
    DATABASE_URI = environ.get("DATABASE_URL")


if environ.get("FLASK_ENV") == "PRODUCTION":
    app_config = Prod_Config
else:
    app_config = Dev_Config
