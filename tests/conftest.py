import pytest
from flask import Flask, g
from flask.testing import FlaskClient
from movie_watchlist import create_app
from movie_watchlist.config import Prod_Config, Test_Config


@pytest.fixture
def app() -> Flask:
    app = create_app(Test_Config)
    yield app


@pytest.fixture
def dev_app() -> Flask:
    app = create_app()
    yield app


@pytest.fixture
def prod_app() -> Flask:
    app = create_app(Prod_Config)
    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email="test@gmail.com", password="umbrella"):
        self._client.get("/auth/login/")
        return self._client.post("/auth/login/", data={"email": email, "password": password})

    def logout(self):
        return self._client.get("/auth/logout/")


@pytest.fixture
def auth(client):
    return AuthActions(client)
