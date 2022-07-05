from flask import Blueprint, current_app, render_template

bp = Blueprint("home", __name__)

@bp.route("/")
def home_page():
    get_movies = current_app.db.execute("SELECT title, director, year, average_rating, movie_id FROM rated_movies")
    return render_template("index.html", movies=get_movies)