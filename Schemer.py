from Sparsec import *


class Ast(object):
    def __init__(self, val):
        self.val = val


class Bool(Ast):
    pass


class Number(Ast):
    pass


class String(Ast):
    pass


class List(Ast):
    pass


class Atom(Ast):
    pass


@Parsec
def ParseString(state):
    return String("".join(Between(Eq('"'), Eq('"'), Many(Ne('"')))(state)))


@Parsec
def ParseAtom(state):
    return Atom(Many1(Alphabet)(state))


@Parsec
def ParseNumber(state):
    return Number(float("".join(Many1(Digit)(state))))


@Parsec
def ParseBool(state):
    return Bool(Choice(Eq("#f"), Eq("#t"))(state))


@Parsec
def ParseList(state):
    return List(SepBy(" ", ParseExpr)(state))


@Parsec
def ParseExpr(state):
    return Choice(ParseBool, ParseString, ParseAtom, ParseNumber)(state)


def ReadExpr(expression):
    state = State(expression)
    re = ParseExpr(state)
    return re


print ReadExpr("1")
