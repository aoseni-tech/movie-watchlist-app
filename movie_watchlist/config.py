from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base config."""

    SECRET_KEY = environ.get("SECRET_KEY")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    DATABASE_URL = environ.get("DB_URL")
    DEBUG = False
    TESTING = False
