from flask import Blueprint, redirect, render_template, request, current_app, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from psycopg.errors import UniqueViolation

from ..forms import RegisterUser, LogIn

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route('/register/', methods=('GET', 'POST'))
def register():
    form = RegisterUser()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        try:
            new_user = current_app.db.execute(
                "INSERT INTO users (email, password) VALUES (%s, %s) RETURNING user_id",
                (email, generate_password_hash(password))
            )

            session["user_id"] = new_user[0]["user_id"]
            flash("Thank you for registering, welcome!", category="success")
            return redirect(url_for("home.home_page"), 302)
        except UniqueViolation as e:
            flash(f"Email '{email}' is already registered", category="error")       

    return render_template('auth/register.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = LogIn()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        try:
            get_user = current_app.db.execute(
                    "SELECT * FROM users WHERE email = %s",
                    (email,)
                )
            user = get_user[0]
        except IndexError:
            pass
        else:
            if check_password_hash(user['password'], password):
                referrer = session.get("referrer_url", url_for("home.home_page"))
                session.clear()
                session["user_id"] = user["user_id"]
                flash("Successful log in, welcome back!", category="success")
                return redirect(referrer, 302)

        flash("Incorrect email or password", category="error")
        
    return render_template('auth/login.html', form=form)


@bp.route('/logout/')
def logout():
    session.clear()
    flash("You have been successfully logged out", category="success")
    return redirect(url_for('home.home_page'))

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get("user_id"):
            referrer = request.url
            session['referrer_url'] = referrer
            flash("You must login/register to continue", category="info")
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view