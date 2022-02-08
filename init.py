from urllib.request import urlretrieve

from sql import init_db


def download_libs():
    libs = [
        ("https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.js", "vue.js"),
        ("https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.min.js", "vue.min.js"),
        (
            "https://cdn.jsdelivr.net/npm/simple-keyboard@3.4.44/build/index.js",
            "simple-keyboard.js",
        ),
    ]

    for lib in libs:
        urlretrieve(lib[0], f"static/lib/{lib[1]}")


def init():
    init_db()
    download_libs()


if __name__ == "__main__":
    init()
