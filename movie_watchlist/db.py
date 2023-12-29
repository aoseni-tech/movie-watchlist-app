from dataclasses import dataclass, field
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from functools import wraps
from typing import Callable
from .schema import commands

from flask import Flask


@dataclass
class Psycopg_Db:
    """Postgresql database connection class for the app"""

    app: Flask = field(default=None)
    conn_pool: ConnectionPool = field(init=False, default=None)

    def __post_init__(self) -> None:
        self.conn_pool = ConnectionPool(self.app.config["DATABASE_URI"], timeout=3.0)

    def query_db(fn: Callable):
        @wraps(fn)
        def inner(*args, **kwargs):
            self_class: "Psycopg_Db" = args[0]
            pool = self_class.conn_pool

            with pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as cur:
                    func_args = fn(*args, **kwargs)
                    cur.execute(*func_args[0], **func_args[1])
                    if cur.rowcount >= 1:
                        return cur.fetchall()
                    return []

        return inner

    @query_db
    def execute(self, *args, **kwargs):
        return (args, kwargs)

def get_db(app: Flask):
    app_db = Psycopg_Db(app)
    return app_db

def init_db(app: Flask):
    db: Psycopg_Db = app.db
    for command in commands:
        db.execute(command)
