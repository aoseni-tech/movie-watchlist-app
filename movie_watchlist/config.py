from os import environ
from dotenv import load_dotenv
from json import loads

load_dotenv()

envSecretResponse = environ.get("AWS_MOVIEWATCHLIST_CONFIG")
envSecretString = loads(envSecretResponse);
envSecret = loads(envSecretString.SecretString);


class Config:
    """Base config."""

    SECRET_KEY = envSecret["SECRET_KEY"]
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"


class Dev_Config(Config):
    """Development configuration"""

    ENV = "development"
    DEBUG = True
    TESTING = False
    DATABASE_URI = envSecret["DEV_DATABASE_URI"]


class Test_Config(Config):
    """Development configuration"""

    ENV = "testing"
    DEBUG = True
    TESTING = True
    DATABASE_URI = envSecret["DEV_DATABASE_URI"]
    WTF_CSRF_ENABLED = False


class Prod_Config(Config):
    """Development configuration"""
    
    DEBUG = False
    TESTING = False
    DATABASE_URI = envSecret["DATABASE_URI"]


if environ.get("FLASK_ENV") == "PRODUCTION":
    app_config = Prod_Config
else:
    app_config = Dev_Config
