from random import randint

word_list = [
    "adieu",
    "hello",
]


def random_word():
    return word_list[randint(0, len(word_list) - 1)]
