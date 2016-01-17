from Sparsec import *


def calculate(expression):
    state = State(expression)
    return Expr(state)


@Parsec
def Expr(state):
    """
    expr ::= term { (+|-) term }*
    """
    term1 = Term(state)
    while True:
        op = Try(OneOf("+-"))(state)
        if not op:
            return term1
        else:
            term2 = Term(state)

        if op == "+":
            term1 += term2
        elif op == "-":
            term1 -= term2


@Parsec
def Term(state):
    """
   term ::= factor { (*|/) factor }*
    """
    factor1 = Factor(state)
    while True:
        op = Try(OneOf("*/"))(state)
        if not op:
            return factor1
        else:
            factor2 = Factor(state)

        if op == "*":
            factor1 *= factor2
        elif op == "/":
            factor1 /= factor2


@Parsec
def Factor(state):
    """
    factor ::= ( expr )
    |   NUM
    """
    return Choice(Between(Eq("("), Eq(")"), Expr), Num)(state)


@Parsec
def Num(state):
    n = Many(Digit)(state)
    return int(n)


if __name__ == "__main__":
    print calculate("3*2*4/(2+2)+2*2/4+2")
    print calculate("2+(3+4)*5")
