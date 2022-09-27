"""Module for handling the messy bits of SQL."""
import logging
import os
import sqlite3
from contextlib import contextmanager
from typing import ContextManager

from const import DB_FILE, EXPRESSION_LENGTH
from expressions import generate_expressions

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


@contextmanager
def sql_context() -> ContextManager[sqlite3.Cursor]:
    """Yeilds a fresh sql cursor to .db file"""
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    try:
        yield cur
    finally:
        con.commit()
        con.close()


def init_db(overwrite=True):
    """Initialises a new database in .db file."""
    logger.info(f"Initializing database with expression length={EXPRESSION_LENGTH}")

    if os.path.exists(DB_FILE):
        logger.info(f"Database {DB_FILE} already exists. Skipping.")
        return

    get_schema_cmds = [
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

    for get_schema_cmd in get_schema_cmds:
        with sql_context() as cur:
            cur.execute(get_schema_cmd)

    for expression, _ in generate_expressions():
        with sql_context() as cur:
            cur.execute(
                """
                INSERT INTO expressionList (expression)
                VALUES (?);
            """,
                (expression,),
            )
    logger.info(f"Database created.")
