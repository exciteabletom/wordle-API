import flask
from werkzeug.exceptions import abort

from sql import get_sql


def get_random_answer():
    """
    Retrieves a random answer from the answerList table

    :rtype: tuple
    :returns: A tuple of len 2: (word_id, word)
    """
    con, cur = get_sql()

    word_id, word = cur.execute(
        """SELECT id, word FROM answerList ORDER BY RANDOM() LIMIT 1"""
    ).fetchone()

    return word_id, word


def get_answer_info(word_id):
    """
    Retrieves an answer from answerList that matches word_id

    :rtype: str
    """
    con, cur = get_sql()

    word = cur.execute(
        """SELECT word FROM answerList WHERE id = (?)""", (word_id,)
    ).fetchone()

    return word


def word_is_valid(word):
    """
    Checks if a word is contained in the wordList table.

    :rtype: bool
    :returns: True if it's in the table, otherwise false
    """
    con, cur = get_sql()
    cur.execute("""SELECT word FROM wordList WHERE word = (?)""", (word,))
    return bool(cur.fetchone())


def id_or_400(request: flask.Request):
    """
    Returns the game id associated with the request. On failure, forces a 400 error response.

    :rtype: int
    """
    try:
        game_id = request.get_json(force=True)["id"]
        key = request.get_json(force=True)["key"]

        con, cur = get_sql()
        cur.execute("""SELECT key FROM game WHERE key = (?)""", (key,))
        assert cur.fetchone()[0] == key
        con.close()

        return game_id
    except (AssertionError, KeyError, TypeError):
        abort(400)


def set_finished(game_id):
    """
    Changes the status of a game to finished
    """
    con, cur = get_sql()
    cur.execute("""UPDATE game SET finished = true WHERE id = (?) """, (game_id,))
    con.commit()
    con.close()


def get_game_answer(game_id):
    """
    Get's the answer associated with a game

    :rtype: str
    """
    con, cur = get_sql()
    cur.execute("""SELECT word FROM game WHERE id = (?)""", (game_id,))
    answer = cur.fetchone()
    con.close()

    return answer[0]
