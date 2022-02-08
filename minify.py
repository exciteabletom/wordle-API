#!/usr/bin/env python3
"""
Minify static files, should be run before starting the production server
"""
import os
import sys
from pathlib import Path
import shutil

from rjsmin import jsmin
from rcssmin import cssmin


def recurse_dir(directory):
    files = []
    for child in directory.iterdir():
        if child.is_dir():
            files.extend(recurse_dir(child))
        elif child.is_file():
            files.append(child)

    return files


def minify_static_files():
    old_dir = os.curdir
    os.chdir(sys.path[0])
    try:
        try:
            shutil.rmtree("static_min")
        except FileNotFoundError:
            pass

        shutil.copytree("static", "static_min")

        files = recurse_dir(Path("./static_min"))

        for file in files:
            try:
                content = file.open("r").read()
            except UnicodeError:
                continue

            if file.name.endswith(".js"):
                min_func = jsmin
            elif file.name.endswith(".css"):
                min_func = cssmin
            else:
                continue

            file.open("w").write(min_func(content))
    finally:  # Ensure that the current dir is not modified by this function
        os.chdir(old_dir)


if __name__ == "__main__":
    minify_static_files()
