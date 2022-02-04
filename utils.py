from random import randint

from werkzeug.exceptions import abort

from sql import get_sql

# Use set for "var in word_set"
# Use list for everything else
word_list = open("word_list.txt", "r").read().split("\n")
word_set = set(word_list)


def random_word():
    return word_list[randint(0, len(word_set) - 1)]


def word_is_valid(word):
    return word in word_set


def get_id_or_400(request):
    try:
        game_id = request.form["id"]
        game_id = int(game_id)
        return game_id
    except (KeyError, TypeError):
        abort(400)


def set_finished(game_id):
    con, cur = get_sql()
    cur.execute("""UPDATE game SET finished = true WHERE id = (?) """, (game_id,))
    con.commit()
    con.close()


def get_answer(game_id):
    con, cur = get_sql()
    cur.execute("""SELECT word FROM game WHERE id = (?)""", (game_id,))
    answer = cur.fetchone()
    con.close()

    return answer
