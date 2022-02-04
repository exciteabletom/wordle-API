import sqlite3
import json

from flask import Flask, render_template, request, abort

from words import random_word


def get_sql():
    con = sqlite3.connect("wordle.db")
    cur = con.cursor()
    return con, cur


app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route("/start_game/")
def start_game():
    con, cur = get_sql()

    word = random_word()
    cur.execute("""INSERT INTO game (word) VALUES (?)""", (word,))
    con.commit()
    con.close()

    return json.dumps({"id": cur.lastrowid})


@app.route("/guess/", methods=["POST"])
def guess_word():
    try:
        game_id = request.form["id"]
        guess = request.form["guess"]
        assert len(guess) == 5
    except (KeyError, AssertionError):
        return abort(400)

    game_id = int(game_id)

    con, cur = get_sql()
    cur.execute("""SELECT word, guesses, finished FROM game WHERE id = (?)""", (game_id,))
    answer, guesses, finished = cur.fetchone()

    # Avoids ValueError if guesses is empty
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

        guess_status.append({
            "char": g_char,
            "status": status_int,
        })

    return json.dumps(guess_status)


if __name__ == '__main__':
    app.run()
