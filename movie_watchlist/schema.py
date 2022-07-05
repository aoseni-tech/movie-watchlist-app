commands = (
    r"""
    CREATE TABLE IF NOT EXISTS users (
        user_id uuid DEFAULT gen_random_uuid () UNIQUE,
        email VARCHAR CHECK (email ~* '^[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$') NOT NULL UNIQUE,
        password VARCHAR NOT NULL,
        PRIMARY KEY (user_id)
    )
    """,
    r"""
    CREATE TABLE IF NOT EXISTS movies (
        user_id uuid REFERENCES users ON DELETE CASCADE,
        movie_id uuid DEFAULT gen_random_uuid () UNIQUE,
        title VARCHAR NOT NULL,
        director VARCHAR NOT NULL CHECK (char_length(director) >= 3),
        year SMALLINT NOT NULL CHECK (year >= 1878),
        casts TEXT [],
        series TEXT [],
        tags TEXT [],
        description TEXT,
        video VARCHAR CHECK (video ~* '^$|^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1,1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'),
        PRIMARY KEY (movie_id)
    )
    """,
    r"""
    CREATE TABLE IF NOT EXISTS ratings (
        user_id uuid NOT NULL REFERENCES users ON DELETE CASCADE,
        movie_id uuid NOT NULL REFERENCES movies ON DELETE CASCADE,
        rating SMALLINT,
        PRIMARY KEY (user_id, movie_id)
    )
    """,
    r"""
    CREATE TABLE IF NOT EXISTS users_movies (
        user_id uuid NOT NULL REFERENCES users ON DELETE CASCADE,
        movie_id uuid NOT NULL REFERENCES movies ON DELETE CASCADE,
        watched BOOLEAN DEFAULT FALSE,
        bookmark BOOLEAN DEFAULT FALSE,
        PRIMARY KEY (user_id, movie_id)
    )
    """,
    """
    CREATE OR REPLACE VIEW rated_movies AS
    SELECT 
            m.user_id,
            m.movie_id,
            title,
            director,
            year,
            casts,
            series,
            tags,
            description, 
            video,
            AVG(r.rating)::NUMERIC(10,1) AS average_rating,
            COUNT(r.rating) AS total_ratings
    FROM movies m
    lEFT JOIN ratings r 
        ON r.movie_id = m.movie_id
    GROUP BY m.movie_id, r.movie_id
    """,
    """
    CREATE OR REPLACE VIEW user_rating AS
    SELECT
            rm.user_id,
            rm.movie_id,
            title,
            director,
            year,
            casts,
            series,
            tags,
            description, 
            video,
            r.rating,
            average_rating,
            total_ratings,
			r.user_id as reviewer
    FROM rated_movies rm
    LEFT JOIN ratings r 
        ON r.movie_id = rm.movie_id
    """,
)
