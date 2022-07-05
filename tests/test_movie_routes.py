from flask.testing import FlaskClient
from flask import Flask, url_for, session

def test_new_movie_form_page(client: FlaskClient, app: Flask, auth):
    with app.app_context():
        auth.login()

        get_response = client.get("/movies/new/")
        assert b"Title" in get_response.data
        assert b"Director" in get_response.data
        assert b"Year" in get_response.data
        assert b"hidden" in get_response.data

        data = {
            "title": "Test movie",
            "director": "Idk",
            "year": 2022,
        }

        post_response = client.post(url_for("movies.movies"), data=data, follow_redirects=True)

        get_movie_id = app.db.execute("SELECT movie_id FROM movies WHERE title = %s", ("Test Movie",))

        movie_id = get_movie_id[-1]["movie_id"]

        assert post_response.status_code == 200
        # assert post_response.request.path == url_for("movies.edit", id=movie_id)
        assert b"Test Movie" in post_response.data
        assert b"Idk" in post_response.data

        data["year"] = 1802
        data["director"] = "mi"
        post_response_invalid = client.post(url_for("movies.movies"), data=data, follow_redirects=True)

        assert post_response_invalid.status_code == 200
        assert post_response_invalid.request.path == url_for("movies.new")
        assert b"Year must be greater than or equal 1878." in post_response_invalid.data
        assert b"Field must be at least 3 characters long." in post_response_invalid.data


# test update route without login
def test_movie_update_form_page(client: FlaskClient, app: Flask, auth):
    get_movie_id = app.db.execute("SELECT movie_id FROM movies WHERE title = %s", ("Test Movie",))

    movie_id = get_movie_id[0]["movie_id"]

    with app.app_context():
        auth.login()
        # test_get_update page
        response = client.get(url_for("movies.edit", id=movie_id))
        assert b"Test Movie" in response.data
        assert b"Idk" in response.data
        assert b"2022" in response.data
        assert b"Cast" in response.data
        assert b"Series" in response.data
        assert b"Tags" in response.data
        assert b"Description" in response.data
        assert b"Video link" in response.data

        # test_post_update page
        data = {
            "title": "Test movie",
            "director": "Idk",
            "year": 2022,
            "casts": "john,david,tom",
            "series": "test1, testN",
            "tags": None,
            "description": "Just testing",
            "video" : "https://www.doesnotexist.com"
        }
        post_response = client.post(url_for("movies.edit", id=movie_id), data=data)
        assert post_response.status_code == 302
        assert post_response.location == url_for("movies.show", id=movie_id)
        assert session.get("_flashes")[0] == ('success', 'Updated movie successfully')

        #test_invalid_data_update
        data = {
            "title": "Test movie",
            "director": "Idk",
            "year": 2022,
            "casts": "john,david,tom",
            "series": "test1, testN",
            "description": "Just testing",
            "video" : "hello"
        }        
        post_response_invalid = client.post(url_for("movies.edit", id=movie_id), data=data)
        assert post_response_invalid.status_code == 200
        assert b"Video link must be a valid url." in post_response_invalid.data

        #test editing another users movie
        auth.login("test@outlook.com", "umbrella")
        unauthorize_edit = client.get(url_for("movies.edit", id=movie_id), follow_redirects=True)
        assert b"You are not authorized for this action" in unauthorize_edit.data

        app.db.execute("DELETE FROM movies WHERE movie_id = %s RETURNING movie_id", (movie_id,))

        #test_not_existing movie
        post_not_exist_movie = client.post(url_for("movies.edit", id=movie_id), data=data)
        assert post_not_exist_movie.status_code == 302
        assert post_not_exist_movie.location == url_for("home.home_page")
        assert session.get("_flashes")[-1] == ('error', 'The movie does not exist or has been deleted')

def test_movie_form_no_login(client: FlaskClient):
    response = client.get("/movies/new/")
    assert response.status_code == 302
    response_2 = client.get("/movies/new/", follow_redirects=True)
    assert response_2.status_code == 200
    assert b"You must login/register to continue" in response_2.data


def test_user_movies_page(client: FlaskClient, app: Flask, auth):
        with app.app_context():
            auth.login()

            data = {
                "title": "Test movie show",
                "director": "Idk",
                "year": 2031,
            }

            data_edit = {
                "title": "Test movie show",
                "director": "Idk",
                "year": 2031,
                "video": "http://www.somevideo.com/",
                "casts": "john,david,tom",
            }

            client.post(url_for("movies.movies"), data=data)

            get_movie_id = app.db.execute("SELECT movie_id FROM movies WHERE title = %s", ("Test Movie Show",))
            movie_id = get_movie_id[0]["movie_id"]

            client.post(url_for("movies.edit", id=movie_id), data=data_edit)

            response = client.get("/movies/")
            assert response.status_code == 200
            assert b"Test Movie Show" in response.data
            assert b"2031" in response.data
            assert b"John" not in response.data
            assert b"http://www.somevideo.com/" not in response.data

            #test movie rating
            client.get(url_for("movies.ratings", id=movie_id, rating="gre"))
            client.get(url_for("movies.ratings", id=movie_id, rating="9"))
            rating_response = client.get(url_for("movies.ratings", id=movie_id, rating="3"))
            assert rating_response.status_code == 302
            assert rating_response.location == url_for("movies.show", id=movie_id)

            #test rating deleted movie
            rate_del_movie = client.get(url_for("movies.ratings", id='0e9eb35a-087c-4cfa-bce7-e5b3d831938d', rating="5"), follow_redirects=True)
            assert b"The movie does not exist or has been deleted" in rate_del_movie.data

            #test showing deleted movie
            show_del_movie = client.get(url_for("movies.show", id='0e9eb35a-087c-4cfa-bce7-e5b3d831938d'), follow_redirects=True)
            assert b"The movie does not exist or has been deleted" in show_del_movie.data
            

            # show movie when logged in
            show_movie_response = client.get(url_for("movies.show", id=movie_id))
            assert show_movie_response.status_code == 200
            assert b"Test Movie Show" in show_movie_response.data
            assert b"Idk" in show_movie_response.data
            assert b"2031" in show_movie_response.data
            assert b"John" in show_movie_response.data
            assert b"David" in show_movie_response.data
            assert b"http://www.somevideo.com/" in show_movie_response.data
            assert b"Remove" in show_movie_response.data
            assert b"Edit" in show_movie_response.data

            #show movie when not logged in
            auth.logout()
            show_movie_response_logout = client.get(url_for("movies.show", id=movie_id))
            assert show_movie_response_logout.status_code == 200
            assert b"Test Movie Show" in show_movie_response_logout.data
            assert b"Idk" in show_movie_response_logout.data
            assert b"2031" in show_movie_response_logout.data
            assert b"John" in show_movie_response_logout.data
            assert b"David" in show_movie_response_logout.data
            assert b"http://www.somevideo.com/" in show_movie_response_logout.data
            assert b"Remove" not in show_movie_response_logout.data
            assert b"Edit" not in show_movie_response_logout.data
                        
            app.db.execute("DELETE FROM movies WHERE title = %s RETURNING title, director, year", ("Test Movie Show",))

def test_movie_delete(client: FlaskClient, app: Flask, auth):
    with app.app_context():
        auth.login()

        data = {
            "title": "Test movie show",
            "director": "Idk",
            "year": 2031,
        }
        client.post(url_for("movies.movies"), data=data)
        get_movie_id = app.db.execute("SELECT movie_id FROM movies WHERE title = %s", ("Test Movie Show",))
        movie_id = get_movie_id[0]["movie_id"]

        delete_data = {"owner": session.get("user_id")}

        response = client.post(url_for("movies.delete", id=movie_id), data=delete_data,follow_redirects=True)

        assert response.status_code == 200
        assert response.request.path == url_for("movies.movies")
        assert b"Movie Test Movie Show - 2031 has been deleted" in response.data

        #test trying to delete none existing movies
        response = client.post(url_for("movies.delete", id=movie_id), data=delete_data,follow_redirects=True)

        assert b"Movie does not exist or have been deleted" in response.data

        #test trying to delete other user movies
        auth.login("test@outlook.com", "umbrella")

        response = client.post(url_for("movies.delete", id=movie_id), data=delete_data,follow_redirects=True)

        assert b"You are not authorized to delete the movie" in response.data


def test_watch_info(client: FlaskClient, app: Flask, auth):
    with app.app_context():
        auth.login()
        data = {
            "title": "Test movie show",
            "director": "Idk",
            "year": 2031,
        }
        client.post(url_for("movies.movies"), data=data)
        get_movie_id = app.db.execute("SELECT movie_id FROM movies WHERE title = %s", ("Test Movie Show",))
        movie_id = get_movie_id[0]["movie_id"]

        watched_response = client.get(url_for("movies.watch", movie_id=movie_id, watched=True, bookmark=False), follow_redirects=True)

        assert watched_response.status_code == 200
        assert watched_response.request.path == url_for("movies.show", id=movie_id)
        assert b"Watched" in watched_response.data
        assert b"Bookmark" in watched_response.data

        bookmark_response = client.get(url_for("movies.watch", movie_id=movie_id, watched=False, bookmark=True), follow_redirects=True)

        assert bookmark_response.status_code == 200
        assert bookmark_response.request.path == url_for("movies.show", id=movie_id)
        assert b"Not watched" in bookmark_response.data
        assert b"Want to watch" in bookmark_response.data

        delete_data = {"owner": session.get("user_id")}

        client.post(url_for("movies.delete", id=movie_id), data=delete_data,follow_redirects=True)