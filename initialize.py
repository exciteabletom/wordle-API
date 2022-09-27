#!/usr/bin/env python3
from urllib.request import urlretrieve

from sql import init_db


def download_js_libs():
    # fmt: off
    libs = [
        ("https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.js", "vue.js"),
        ("https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.min.js", "vue.min.js"),
        ("https://cdn.jsdelivr.net/npm/simple-keyboard@3.4.44/build/index.js", "simple-keyboard.js"),
    ]
    # fmt: on

    for lib in libs:
        urlretrieve(lib[0], f"static/lib/{lib[1]}")


if __name__ == "__main__":
    init_db()
    download_js_libs()
