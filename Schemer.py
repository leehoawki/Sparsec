from Sparsec import *


class LispVal(object):
    def __init__(self, val):
        self.val = val


@Parsec
def ParseString(state):
    pass


@Parsec
def ParseAtom(state):
    pass


@Parsec
def ParseNumber(state):
    pass


@Parsec
def ParseBool(state):
    pass


@Parsec
def ParseList(state):
    pass


@Parsec
def ParseExpr(state):
    return Choice(ParseBool, ParseAtom, ParseString, ParseNumber)


def ReadExpr(expression):
    state = State(expression)
    re = ParseExpr(state)
