import json
import uuid

from flask import Flask, render_template, request, abort, make_response
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from const import EXPRESSION_LENGTH
from expressions import is_valid_expression, evalute_expression
from sql import get_sql
from utils import get_random_expression
from utils import id_or_400
from utils import set_finished, get_game_answer

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
CORS(app)


def api_response(json_data):
    resp = make_response(json.dumps(json_data))
    resp.content_type = "application/json; charset=utf-8"
    return resp


# Frontend views
@app.route("/")
def index():
    return render_template("index.html")


# API endpoints
@app.route("/api/v1/start_game/", methods=["POST"])
def start_game():
    """Starts a new game"""
    game_id, expression = get_random_expression()
    result = evalute_expression(expression)
    con, cur = get_sql()
    key = str(uuid.uuid4())
    cur.execute("""INSERT INTO game (expression, key) VALUES (?, ?)""", (expression, key))
    con.commit()
    con.close()

    return api_response({"id": cur.lastrowid, "key": key, "wordID": game_id, "result": result})


@app.route("/api/v1/guess/", methods=["POST"])
def guess_word():
    guess = request.get_json(force=True)["guess"]

    if not (len(guess) == EXPRESSION_LENGTH and not guess.isalpha() and is_valid_expression(guess)):
        return abort(400, "Invalid expression!")

    game_id = id_or_400(request)

    con, cur = get_sql()
    cur.execute("""SELECT expression, guesses, finished FROM game WHERE id = (?)""", (game_id,))
    answer, guesses, finished = cur.fetchone()

    guesses = guesses.split(",")

    if len(guesses) > EXPRESSION_LENGTH + 1 or finished:
        return abort(403)

    guesses.append(guess)
    guesses = ",".join(guesses)

    if guesses[0] == ",":
        guesses = guesses[1:]

    cur.execute("""UPDATE game SET guesses = (?) WHERE id = (?)""", (guesses, game_id))
    con.commit()
    con.close()

    guess_status = [{"letter": g_char, "state": 0} for g_char in guess]
    guessed_pos = set()

    for a_pos, a_char in enumerate(answer):
        if a_char == guess[a_pos]:
            guessed_pos.add(a_pos)
            guess_status[a_pos] = {
                "letter": guess[a_pos],
                "state": 2,
            }

    for g_pos, g_char in enumerate(guess):
        if g_char not in answer or guess_status[g_pos]["state"] != 0:
            continue

        positions = []
        f_pos = answer.find(g_char)
        while f_pos != -1:
            positions.append(f_pos)
            f_pos = answer.find(g_char, f_pos + 1)

        for pos in positions:
            if pos in guessed_pos:
                continue
            guess_status[g_pos] = {
                "letter": g_char,
                "state": 1,
            }
            guessed_pos.add(pos)
            break

    return api_response(guess_status)


@app.route("/api/v1/finish_game/", methods=["POST"])
def finish_game():
    game_id = id_or_400(request)
    set_finished(game_id)
    answer = get_game_answer(game_id)

    return api_response({"answer": answer})


if __name__ == "__main__":
    app.run()
