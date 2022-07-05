from flask import Flask
from movie_watchlist import db
import pytest
import psycopg_pool

def test_config(app: Flask, prod_app: Flask, dev_app: Flask):
    assert app.config["TESTING"] == True
    assert app.config["DEBUG"] == True
    assert dev_app.config["TESTING"] == False
    assert dev_app.config["DEBUG"] == True
    assert prod_app.config["TESTING"] == False
    assert prod_app.config["DEBUG"] == False
    assert isinstance(app.db, db.Psycopg_Db)
    assert isinstance(prod_app.db, db.Psycopg_Db)


def test_db(app: Flask, prod_app: Flask):
    get_test_app_dbversion = app.db.execute("SELECT version()")
    get_prod_app_dbversion = prod_app.db.execute("SELECT version()")
    assert len(get_test_app_dbversion) == 1
    assert len(get_prod_app_dbversion) == 1

def test_db_error(app: Flask):
    app.config["DATABASE_URI"] = "wrong_uri"
    app.db = db.Psycopg_Db(app)
    with pytest.raises(psycopg_pool.PoolTimeout):
        app.db.execute("SELECT version()")
