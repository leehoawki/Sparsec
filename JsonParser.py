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
    a = {}
    while True:
        Trim(state)
        key = String(state)
        Trim(state)
        Eq(":")(state)
        Trim(state)
        val = Value(state)
        Trim(state)
        a[key] = val
        s = Choice(Eq(","), Eq("}"))(state)
        if s == "}":
            break
        elif s == ",":
            continue
    return a


@Parsec
def Array(state):
    Eq("[")(state)
    a = []
    while True:
        Trim(state)
        re = Value(state)
        a.append(re)
        Trim(state)
        s = Choice(Eq(","), Eq("]"))(state)
        if s == "]":
            break
        elif s == ",":
            continue
    return a


@Parsec
def String(state):
    return "".join(Between(Eq('"'),Eq('"'),Many(Ne('"')))(state))


@Parsec
def Null(state):
    Eq("null")(state)
    return None


@Parsec
def True(state):
    Eq("true")(state)
    return True


@Parsec
def False(state):
    Eq("false")(state)
    return False


@Parsec
def Number(state):
    n = "".join(Many(OneOf("1234567890-+."))(state))
    return float(n)


@Parsec
def Value(state):
    re = Choice(Null, True, False, String, Object, Array, Number)(state)
    return re


if __name__ == "__main__":
    print load("""{
        "programmers": [{
            "firstName": "Brett",
            "lastName": "McLaughlin",
            "email": "aaaa"
        }, {
            "firstName": "Jason",
            "lastName": "Hunter",
            "email": "bbbb"
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
    }""")
