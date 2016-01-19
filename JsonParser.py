from Sparsec import *


def load(s):
    state = State(s)
    Trim(state)
    re = Choice(Object, Array)(state)
    Trim(state)
    EOF(state)
    return re


@Parsec
def Trim(state):
    Many(OneOf(" \r\n"))(state)


@Parsec
def Object(state):
    Eq("{")(state)

    @Parsec
    def parse(state):
        Trim(state)
        key = String(state)
        Trim(state)
        Eq(":")(state)
        Trim(state)
        val = Value(state)
        Trim(state)
        return key, val

    re = dict(SepBy(",", parse)(state))
    Eq("}")(state)
    return re


@Parsec
def Array(state):
    Eq("[")(state)

    @Parsec
    def parse(state):
        Trim(state)
        re = Value(state)
        Trim(state)
        return re

    re = SepBy(",", parse)(state)
    Eq("]")(state)
    return re


@Parsec
def String(state):
    return "".join(Between(Eq('"'), Eq('"'), Many(Ne('"')))(state))


@Parsec
def Null(state):
    Eq("null")(state)
    return None


@Parsec
def Number(state):
    n = "".join(Many(OneOf("1234567890-+."))(state))
    try:
        return float(n)
    except ValueError:
        raise SparseError("Can not convert %s to Number " % n)


@Parsec
def Bool(state):
    return {"true": True, "false": False}.get(Choice(Eq("true"), Eq("false"))(state))


@Parsec
def Value(state):
    return Choice(Null, Bool, String, Object, Array, Number)(state)


if __name__ == '__main__':
    long_text = """{
            "programmers": [{
                "firstName": "Brett",
                "lastName": "McLaughlin",
                "email": "aaaa",
                "age":12,
                "isshit":true
            }, {
                "firstName": "Jason",
                "lastName": "Hunter",
                "email": "bbbb",
                "isshit":false
            }, {
                "firstName": "Elliotte",
                "lastName": "Harold",
                "email": "cccc"
            }],
            "authors": [{
                "firstName": "Isaac",
                "lastName": "Asimov",
                "genre": "sciencefiction"
            }, {
                "firstName": "Tad",
                "lastName": "Williams",
                "genre": "fantasy"
            }, {
                "firstName": "Frank",
                "lastName": "Peretti",
                "genre": "christianfiction"
            }],
            "musicians": [{
                "firstName": "Eric",
                "lastName": "Clapton",
                "instrument": "guitar"
            }, {
                "firstName": "Sergei",
                "lastName": "Rachmaninoff",
                "instrument": "piano"
            }]
        }
        """

    print load(long_text)
