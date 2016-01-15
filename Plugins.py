from Sparsec import *


def One(item):
    @Parsec
    def parse(state):
        re = state.next()
        if re != item:
            raise ExpectingError(item, re)
        return re

    return parse


def OneOf(items):
    @Parsec
    def parse(state):
        re = state.next()
        if re not in items:
            raise ExpectingError(items, re)
        return re

    return parse


@Parsec
def Space(state):
    re = state.next()
    if re != ' ':
        raise ExpectingError("space char", re)
    return re


@Parsec
def Digit(state):
    re = state.next()
    if not re.isdigit():
        raise ExpectingError("Digit", re)
    return re


def Try(parsec):
    @Parsec
    def parse(state):
        try:
            state.backup()
            return parsec(state)
        except SparseError:
            state.restore()

    return parse


def Many(parsec):
    @Parsec
    def parse(state):
        c = Try(parsec)
        items = ""
        item = c(state)
        while item:
            items += item
            item = c(state)
        return items

    return parse


def Ne(item):
    @Parsec
    def parse(state):
        re = state.next()
        if re == item:
            raise ExpectingError("Not %s" % item, re)
        return re

    return parse


def Eq(items):
    @Parsec
    def parse(state):
        for item in items:
            re = state.next()
            if re != item:
                raise ExpectingError(item, re)
            return re

    return parse


def Choice(*parsecs):
    @Parsec
    def parse(state):
        for c in parsecs:
            re = Try(c)(state)
            if re:
                return re
        raise SparseError("No choice can match.")

    return parse


@Parsec
def EOF(state):
    if state.has_next():
        raise ExpectingError("EOF", state.get_rest())
