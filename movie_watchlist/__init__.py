from flask import Flask, g, session
from .config import Dev_Config
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


def create_app(app_config=Dev_Config):
    app = Flask(__name__)

    app.config.from_object(app_config)
    app.config["SECURITY_CSRF_COOKIE_NAME"] = "XSRF-TOKEN"

    # Don't have csrf tokens expire (they are invalid after logout)
    app.config["WTF_CSRF_TIME_LIMIT"] = None

    # You can't get the cookie until you are logged in.
    app.config["SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS"] = True
    
    csrf.init_app(app)

    from .db import get_db, init_db
    app.db = get_db(app)
    init_db(app)

    from .routes import index, movie, auth
    app.register_blueprint(index.bp)
    app.register_blueprint(movie.bp)
    app.register_blueprint(auth.bp)

    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            g.user = app.db.execute(
                'SELECT email, user_id FROM users WHERE user_id = %s', (user_id,)
            )[0]

    @app.context_processor
    def inject_user():
        return dict(user=g.user)

    return app
