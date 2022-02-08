import json
import uuid

from flask import Flask, render_template, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

from utils import set_finished, get_answer, word_is_valid, id_or_400, get_answer_info
from sql import get_sql

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

limiter = Limiter(
    app,
    key_func=get_remote_address,
)


@app.context_processor
def inject_debug():
    return dict(debug=app.debug)


# Frontend views
@app.route("/")
def index():
    return render_template("index.html")


# API endpoints
@app.route("/api/v1/start_game/", methods=["POST"])
@limiter.limit("4/second;120/minute;600/hour;4000/day")
def start_game():
    """
    Starts a new game
    :return: {"id": game_id}
    """
    word_id = None
    try:
        word_id = int(request.json["wordID"])
    except (KeyError, TypeError, ValueError):
        pass

    con, cur = get_sql()

    key = str(uuid.uuid4())

    word_id, word = get_answer_info(word_id)

    cur.execute("""INSERT INTO game (word, key) VALUES (?, ?)""", (word, key))
    con.commit()
    con.close()

    return json.dumps({"id": cur.lastrowid, "key": key, "wordID": word_id})


@app.route("/api/v1/guess/", methods=["POST"])
def guess_word():
    try:
        guess = request.get_json(force=True)["guess"]
        assert len(guess) == 5
        assert guess.isalpha()
        assert word_is_valid(guess)
    except AssertionError:
        return abort(400, "Invalid word")

    game_id = id_or_400(request)

    con, cur = get_sql()
    cur.execute(
        """SELECT word, guesses, finished FROM game WHERE id = (?)""", (game_id,)
    )
    answer, guesses, finished = cur.fetchone()

    guesses = guesses.split(",")

    if len(guesses) > 6 or finished:
        return abort(403)

    guesses.append(guess)
    guesses = ",".join(guesses)

    if guesses[0] == ",":
        guesses = guesses[1:]

    cur.execute("""UPDATE game SET guesses = (?) WHERE id = (?)""", (guesses, game_id))
    con.commit()
    con.close()

    guess_status = []

    for g_pos, g_char in enumerate(guess):
        status_int = 0
        if g_char in answer:
            status_int += 1
            for a_pos, a_char in enumerate(answer):
                if g_char == a_char and g_pos == a_pos:
                    status_int += 1

        guess_status.append(
            {
                "letter": g_char,
                "state": status_int,
            }
        )

    return json.dumps(guess_status)


@app.route("/api/v1/finish_game/", methods=["POST"])
def finish_game():
    game_id = id_or_400(request)
    set_finished(game_id)
    answer = get_answer(game_id)

    return json.dumps({"answer": answer})


if __name__ == "__main__":
    app.run()
