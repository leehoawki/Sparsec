class Parsec(object):
    def __init__(self, parserc, *args, **kwargs):
        self.parsec = parserc
        super(Parsec, self).__init__(*args, **kwargs)

    def __call__(self, state):
        if not isinstance(state, State):
            raise SparseError("Only State target is acceptable.")
        return self.parsec(state)

    def then(self, c):
        @Parsec
        def func(state):
            self.parsec(state)
            return c(state)

        return func

    def bind(self, c):
        @Parsec
        def func(state):
            binder = c(self.parsec(state))
            return binder(state)

        return func

    def __repr__(self):
        return self.parsec.__repr__()


class SparseError(Exception):
    def __init__(self, message):
        super(SparseError, self).__init__("Parsing Error : %s" % message)


class ExpectingError(SparseError):
    def __init__(self, expected, result):
        super(ExpectingError, self).__init__("Expecting %s, but got %s" % (expected, result))


class State(object):
    def __init__(self, data):
        self.data = data
        self.index = 0
        self.tran = []

    def next(self):
        if 0 <= self.index < len(self.data):
            re = self.data[self.index]
            self.index += 1
            return re
        else:
            raise SparseError("nothing to sparse, EOF.")

    def backup(self):
        self.tran.append(self.index)
        return self.index

    def commit(self):
        self.tran.pop()

    def restore(self):
        self.index = self.tran.pop()

    def has_next(self):
        if self.index < len(self.data):
            return True
        else:
            return False

    def get_rest(self):
        return self.data[self.index:]


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
            re = parsec(state)
            state.commit()
            return re
        except SparseError:
            state.restore()

    return parse


def Many(parsec):
    @Parsec
    def parse(state):
        c = Try(parsec)
        items = []
        item = c(state)
        while item:
            items.append(item)
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
        return items

    return parse


def Choice(*parsecs):
    @Parsec
    def parse(state):
        for c in parsecs:
            re = Try(c)(state)
            if re is not None:
                return re
        raise SparseError("No choice can match.")

    return parse


@Parsec
def EOF(state):
    if state.has_next():
        raise ExpectingError("EOF", state.get_rest())


def Between(start, end, parser):
    @Parsec
    def parse(state):
        start(state)
        re = parser(state)
        end(state)
        return re

    return parse


def SepBy(sep, parser):
    @Parsec
    def parse(state):
        c = Try(Eq(sep).then(parser))
        items = []
        item = Try(parser)(state)
        while item is not None:
            items.append(item)
            item = c(state)
        return items

    return parse
