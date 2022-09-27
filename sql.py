"""Module for handling the messy bits of SQL."""
import sqlite3

from expressions import generate_expressions


def get_sql():
    """Gets a fresh sql connection and cursor to ./nerdle.db"""
    con: sqlite3.Connection = sqlite3.connect("nerdle.db")
    cur: sqlite3.Cursor = con.cursor()
    return con, cur


def init_db():
    """
    Initialises a new database in ./nerdle.db
    """
    con, cur = get_sql()

    schemas = [
        """DROP TABLE IF EXISTS answerList;""",
        """DROP TABLE IF EXISTS expressionList;""",
        """DROP TABLE IF EXISTS game;""",
        """
        CREATE TABLE expressionList (
            id INTEGER NOT NULL PRIMARY KEY,
            expression TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE game (
            id INTEGER NOT NULL PRIMARY KEY,
            expression TEXT NOT NULL,
            finished BOOL NOT NULL DEFAULT false,
            guesses TEXT default "",
            key TEXT NOT NULL,
            FOREIGN KEY (expression) REFERENCES answerList(expression)
        );
        """,
    ]

    for schema in schemas:
        cur.execute(schema)

    for expression, answer in generate_expressions():
        cur.execute(
            """
            INSERT INTO expressionList (expression)
            VALUES (?);
        """,
            (expression,),
        )

    con.commit()
    con.close()
