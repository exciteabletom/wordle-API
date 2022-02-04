"""
Module for handling the messy bits of SQL.
"""
import sqlite3


def get_sql():
    con: sqlite3.Connection = sqlite3.connect("wordle.db")
    cur: sqlite3.Cursor = con.cursor()
    return con, cur


def init_db():
    con, cur = get_sql()

    cur.execute(
        """
        CREATE TABLE game (
            id INTEGER NOT NULL PRIMARY KEY,
            word TEXT NOT NULL,
            finished BOOL NOT NULL DEFAULT false,
            guesses TEXT default ""
        );
    """
    )
    con.commit()
    con.close()
