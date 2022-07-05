from flask import Flask
from flask.testing import FlaskClient

def test_index(client: FlaskClient, app: Flask, auth):
    with app.app_context():
        response = client.get("/")
        assert b"LOG IN" in response.data
        assert b"REGISTER" in response.data
        auth.login()
        response = client.get("/")
        assert b"LOG OUT" in response.data
        assert b"MY LIST" in response.data
        assert b"MOVIES" in response.data        
        assert b"Title" in response.data        
        assert b"Director" in response.data        
        assert b"Year" in response.data        
    