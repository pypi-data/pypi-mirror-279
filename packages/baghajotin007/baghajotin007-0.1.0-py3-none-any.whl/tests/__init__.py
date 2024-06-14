# This will import the `add` and `subtract` functions from module.py
# and make them available directly from mypackage.

from .module import add, subtract


def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
