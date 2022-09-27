import logging
from typing import Tuple

import flask
from werkzeug.exceptions import abort

from sql import get_sql

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def get_random_expression() -> Tuple[str, str]:
    """Retrieves a random expression from the expressionList table."""
    con, cur = get_sql()
    exp_id, expression = cur.execute("""SELECT id, expression FROM expressionList ORDER BY RANDOM() LIMIT 1""").fetchone()
    logger.info(f"Fetched:{exp_id=} {expression=}")
    return exp_id, expression


def get_answer_info(game_id):
    """Retrieves an answer from answerList that matches word_id"""
    con, cur = get_sql()
    answer = cur.execute("""SELECT answer FROM answerList WHERE id = (?)""", (game_id,)).fetchone()
    return answer


def id_or_400(request: flask.Request):
    """Returns the game id associated with the request. On failure, forces a 400 error response."""
    try:
        game_id = request.get_json(force=True)["id"]
        key = request.get_json(force=True)["key"]
        logger.info(f"Got game: {game_id}, {key}")

        con, cur = get_sql()
        cur.execute("""SELECT key FROM game WHERE key = (?)""", (key,))
        assert cur.fetchone()[0] == key
        con.close()

        return game_id
    except (AssertionError, KeyError, TypeError):
        abort(400)


def set_finished(game_id):
    """Changes the status of a game to finished"""
    con, cur = get_sql()
    cur.execute("""UPDATE game SET finished = true WHERE id = (?) """, (game_id,))
    con.commit()
    con.close()


def get_game_answer(game_id):
    """Get's the answer associated with a game"""
    con, cur = get_sql()
    cur.execute("""SELECT expression FROM game WHERE id = (?)""", (game_id,))
    answer = cur.fetchone()
    con.close()
    return answer[0]
