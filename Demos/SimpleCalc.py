from Sparsec import *
from operator import add, sub, mul, div

ops = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": div
}


def calculate(expression):
    state = State(expression)
    return Expr(state)


@Parsec
def Expr(state):
    """
    expr ::= term { (+|-) term }*
    """
    re = Term(state)

    @Parsec
    def terms(state):
        op = OneOf("+-")(state)
        t = Term(state)
        return (op, t)

    for op, t in Many(terms)(state):
        re = ops[op](re, t)
    return re


@Parsec
def Term(state):
    """
   term ::= factor { (*|/) factor }*
    """
    re = Factor(state)

    @Parsec
    def factors(state):
        op = OneOf("*/")(state)
        f = Factor(state)
        return (op, f)

    for op, f in Many(factors)(state):
        re = ops[op](re, f)
    return re


@Parsec
def Factor(state):
    """
    factor ::= ( expr )
    |   NUM
    """
    return Choice(Between(Eq("("), Eq(")"), Expr), Num)(state)


@Parsec
def Num(state):
    n = "".join(Many(Digit)(state))
    return int(n)


if __name__ == "__main__":
    print calculate("3*2*4/(2+2)+2*2/4+2")
    print calculate("2+(3+4)*5")
