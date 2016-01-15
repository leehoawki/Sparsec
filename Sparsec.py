class Parsec(object):
    def __init__(self, parserc, *args, **kwargs):
        self.parsec = parserc
        super(Parsec, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.parsec(*args, **kwargs)

    def then(self, c):
        def parse(state):
            self.parsec(state)
            return c(state)


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
        self.tran = None

    def next(self):
        if 0 <= self.index < len(self.data):
            re = self.data[self.index]
            self.index += 1
            return re
        else:
            raise SparseError("nothing to sparse, EOF.")

    def backup(self):
        self.tran = self.index
        return self.index

    def commit(self, tran):
        self.tran = None

    def restore(self):
        self.index = self.tran
        self.tran = None

    def has_next(self):
        if self.index < len(self.data):
            return True
        else:
            return False

    def get_rest(self):
        return self.data[self.index:]