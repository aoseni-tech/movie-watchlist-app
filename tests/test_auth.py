import pytest
from flask import url_for, g, session

def test_register(client, app):
    assert client.get("/auth/register/").status_code == 200
    response = client.post(
        "/auth/register/", data={"email": "tester@gmail.com", "password": "tester", "confirm": "tester"}
    )
    assert response.headers["Location"] == url_for("home.home_page")

    assert app.db.execute("SELECT * FROM users WHERE email = %s", ("tester@gmail.com",)) is not None

    app.db.execute("DELETE FROM users WHERE email = %s RETURNING user_id", ("tester@gmail.com",))


@pytest.mark.parametrize(
    ("email", "password", "confirm", "message"),
    (
        ("", "", "", b"Email field is required"),
        ("a@gmail.com", "", "", b"Password is required."),
        ("a@gmail.com", "tester", "testo", b"Passwords must match."),
        ("test@gmail.com", "testor", "testor", b"Email &#39;test@gmail.com&#39; is already registered")
    ),
)
def test_register_validate_input(client, email, password, confirm, message):
    client.get("/auth/register/")
    response = client.post("/auth/register/", data={"email": email, "password": password, "confirm": confirm})
    assert message in response.data

def test_login(client, auth, app):
    assert client.get("/auth/login/").status_code == 200
    response = auth.login()
    assert response.location == url_for("home.home_page")

    user_id = app.db.execute("SELECT user_id FROM users WHERE email = %s", ("test@gmail.com",))

    client.get("/")
    assert session["user_id"] == user_id[0]["user_id"]
    assert g.user["email"] == "test@gmail.com"

@pytest.mark.parametrize(
    ("email", "password"),
    (   
        ("idk@gmail.com", "qwerty"),
        ("test@gmail.com", "qwerty")
    )
)
def test_login_validate_input(auth, email, password):
    response = auth.login(email, password)
    assert b"Incorrect email or password" in response.data

def test_logout(auth):
    auth.login()
    auth.logout()
    assert session.get("user_id") is None
