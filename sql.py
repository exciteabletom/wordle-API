"""
Module for handling the messy bits of SQL.
"""
import random
import sqlite3


def get_sql():
    """
    Gets a fresh sql connection and cursor to ./wordle.db

    :rtype: tuple[sqlite3.Connection, sqlite3.Cursor]
    """
    con: sqlite3.Connection = sqlite3.connect("wordle.db")
    cur: sqlite3.Cursor = con.cursor()
    return con, cur


def init_db():
    """
    Initialises a new database in ./wordle.db
    """
    con, cur = get_sql()

    schemas = [
        """
        CREATE TABLE wordList (
            id INTEGER NOT NULL PRIMARY KEY,
            word TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE answerList (
            id INTEGER NOT NULL PRIMARY KEY,
            word TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE game (
            id INTEGER NOT NULL PRIMARY KEY,
            word TEXT NOT NULL,
            finished BOOL NOT NULL DEFAULT false,
            guesses TEXT default "",
            key TEXT NOT NULL,
            FOREIGN KEY (word) REFERENCES wordList(word)
        );
        """,
    ]

    for schema in schemas:
        cur.execute(schema)

    word_list = open("word_list.txt", "r").read().split("\n")
    answer_list = open("answer_list.txt", "r").read().split("\n")
    random.shuffle(word_list)
    random.shuffle(answer_list)

    for word in word_list:
        cur.execute(
            """
            INSERT INTO wordList (word)
            VALUES (?);
        """,
            (word,),
        )

    for word in answer_list:
        cur.execute(
            """
            INSERT INTO answerList (word)
            VALUES (?);
        """,
            (word,),
        )

    con.commit()
    con.close()
