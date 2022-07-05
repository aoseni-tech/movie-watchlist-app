from flask import Blueprint, redirect, render_template, request, current_app, url_for, session, flash
from ..forms import AddMovie, UpdateMovie
from .auth import login_required

bp = Blueprint("movies", __name__, url_prefix="/movies")


@bp.route("/", endpoint="movies", methods=("GET", "POST"))
@bp.get("/new/", endpoint="new")
@login_required
def index():
    form = AddMovie()
    user_id = session.get("user_id")

    if request.endpoint == "movies.movies":
        if request.method == "GET":
            user_movies = current_app.db.execute(
                "SELECT title, director, year, movie_id FROM movies WHERE user_id = %s",
                (user_id,)
                )

            return render_template("movies.html", movies=user_movies)

        elif form.validate_on_submit():

            new_movie = (form.title.data, form.director.data, form.year.data, user_id)
            posted_movie = current_app.db.execute(
                """INSERT INTO movies (title, director, year, user_id)
                    VALUES (%s, %s, %s, %s) RETURNING movie_id
                """,
                new_movie,
            )

            movie_id = posted_movie[0].pop("movie_id")

            flash("Movie added successfully", category="success")
            return redirect(url_for(".edit", id=movie_id))

        session["form_obj"] = [form.data, form.errors]
        return redirect(url_for(".new"))

    form_obj = [{}, {}]
    if "form_obj" in session:
        form_obj = session.pop("form_obj")

    return render_template("movieforms/add.html", form=form, form_obj=form_obj)

@bp.get("/<uuid:id>/", endpoint="show")
def show_movie(id):
    user_id = session.get('user_id')
    try:
        get_movie: list
        user_watch = {"watched": False, "bookmark": False}
        if user_id:
            get_movie = current_app.db.execute(
                """
                    SELECT * FROM user_rating
                    WHERE movie_id = %s AND reviewer = %s
                """, 
                (id,user_id)
                )

            get_user_watch = current_app.db.execute("""
                                                    SELECT watched, bookmark 
                                                    FROM users_movies
                                                    WHERE user_id = %s AND movie_id = %s
                                                    """, (user_id,id))
            if len(get_user_watch):                                                
                user_watch["watched"] = get_user_watch[0]["watched"]
                user_watch["bookmark"] = get_user_watch[0]["bookmark"]
        
        if not user_id or not get_movie:
            get_movie = current_app.db.execute(
                """
                    SELECT * FROM rated_movies
                    WHERE movie_id = %s
                """, 
                (id,)
                )          
        

        movie = get_movie[0]
        movie["watched"] = user_watch["watched"]
        movie["bookmark"] = user_watch["bookmark"]

        return render_template("show_movie.html", movie=movie)
    except IndexError:
        flash("The movie does not exist or has been deleted", category="error")
        return redirect(url_for("home.home_page"))    

@bp.route("/<uuid:id>/edit/", endpoint="edit", methods=("GET", "POST"))
@login_required
def edit_movie(id):
    user_id = session.get('user_id')
    get_movie = current_app.db.execute(
        """
            SELECT *
            FROM movies
            WHERE movie_id = %s
        """,
        (id,),
    )

    if len(get_movie) == 0:
        flash("The movie does not exist or has been deleted", category="error")
        return redirect(url_for("home.home_page"))
    
    movie = get_movie[0]

    if user_id != movie["user_id"]:
        flash("You are not authorized for this action", category="error")
        return redirect(url_for("home.home_page"))

    form = UpdateMovie(**movie)

    if form.validate_on_submit():
        current_app.db.execute(
            """UPDATE movies
            SET title = %s, director = %s,year = %s,casts = %s,series = %s,tags = %s,description = %s, video = %s, user_id = %s
            WHERE movie_id = %s RETURNING movie_id
                """,
                (form.title.data, form.director.data, form.year.data, form.casts.data, form.series.data, form.tags.data, form.description.data,form.video.data,user_id,id)
            )
        flash("Updated movie successfully", category="success")
        return redirect(url_for("movies.show", id=id))

    return render_template("movieforms/update.html", form=form, movie_id=id)

@bp.get("/<uuid:id>/ratings/", endpoint="ratings")
@login_required
def ratings(id):
    user_id = session.get('user_id')
    get_rating = request.args.get("rating")

    if not get_rating.isdigit() or int(get_rating) not in range(0,6):
        rating = None
    else:
        rating = int(get_rating)

    get_movie = current_app.db.execute(
        """
            SELECT title
            FROM movies
            WHERE movie_id = %s
        """,
        (id,),
    )

    if len(get_movie) == 0:
        flash("The movie does not exist or has been deleted", category="error")
        return redirect(url_for("home.home_page"))

    if rating:    
        current_app.db.execute(
        """
            INSERT INTO ratings (user_id, movie_id, rating)
            VALUES (%s,%s,%s)
            ON CONFLICT ON CONSTRAINT ratings_pkey
            DO
                UPDATE set rating = EXCLUDED.rating
            RETURNING rating
        """,
        (user_id, id, rating)
        )
    else:
        current_app.db.execute(
        """
            INSERT INTO ratings (user_id, movie_id)
            VALUES (%s,%s)
            ON CONFLICT ON CONSTRAINT ratings_pkey
            DO
                UPDATE set rating = EXCLUDED.rating
            RETURNING rating
        """,
        (user_id, id)
        )

    return redirect(url_for(".show", id=id))

@bp.post("/<uuid:id>/delete/", endpoint="delete")
@login_required
def delete(id):
    movie_owner = request.form.get('owner')
    session_user = session.get('user_id')

    if str(movie_owner) == str(session_user):
        try:
            get_del_movie = current_app.db.execute(
                            """
                            DELETE FROM movies 
                            WHERE movie_id = %s 
                            RETURNING title, year
                            """, (id,))
            del_movie = get_del_movie[0]
        except IndexError:
            flash("Movie does not exist or have been deleted", category="error")
        else:
            flash(f"Movie {del_movie['title']} - {del_movie['year']} has been deleted", category="success")
    else:
        flash("You are not authorized to delete the movie", category="error")
    return redirect(url_for("movies.movies"))

@bp.get("/<uuid:movie_id>/watch/", endpoint="watch")
@login_required
def watch(movie_id):
    watched = request.args.get("watched")
    bookmark = request.args.get("bookmark")

    user_id = session.get('user_id')

    current_app.db.execute(
                            """
                            INSERT INTO users_movies 
                            (user_id, movie_id,bookmark, watched)
                            VALUES(%s,%s,%s,%s) 
                            ON CONFLICT (user_id, movie_id)
                            DO 
                                UPDATE SET 
                                        bookmark = EXCLUDED.bookmark,
                                        watched = EXCLUDED.watched
                            RETURNING user_id, movie_id, watched,bookmark
                            """, (user_id,movie_id,bookmark, watched))
    
    return redirect(url_for(".show", id=movie_id))

                