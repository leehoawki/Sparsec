from Sparsec import *


###########Types and Builtin###############

class Env(dict):
    def __init__(self, parent=None, para={}):
        self.parent = parent
        self.update(para)

    def get(self, k, d=None):
        if k in self:
            return self[k]
        elif self.parent:
            return self.parent.get(k, d)
        else:
            return None


class Ast(object):
    def __init__(self, val):
        self.val = val

    def accept(self, visitor):
        return visitor.visit(self)


class Bool(Ast):
    a = {"#t": True, "#f": False}

    def __init__(self, val):
        self.val = self.__class__.a.get(val)


class Number(Ast):
    pass


class String(Ast):
    pass


class List(Ast):
    pass


class Atom(Ast):
    pass


#############Eval and Apply################

class Visitor(object):
    def visit(self, visited):
        return getattr(self, "visit%s" % visited.__class__.__name__)(visited)


class EvalVisitor(Visitor):
    def __init__(self, env):
        self.env = env

    def visitString(self, visited):
        return visited.val

    def visitNumber(self, visited):
        return visited.val

    def visitAtom(self, visited):
        return self.env.get(visited.val)

    def visitList(self, visited):
        first = visited.val[0]
        if first.val == "if":
            con, e1, e2 = visited.val[1:]
            exp = e1 if con.accept(self) else e2
            return exp.accept(self)S
        func = first.accept(self)
        args = map(lambda x: x.accept(self), visited.val[1:])
        return func(*args)

    def visitBool(self, visited):
        return visited.val


#################Parser####################

@Parsec
def ParseString(state):
    return String("".join(Between(Eq('"'), Eq('"'), Many(Ne('"')))(state)))


@Parsec
def ParseAtom(state):
    return Atom("".join(Many1(Choice(Alphabet, OneOf("!#$%&|*+-/:<=>?@^_~")))(state)))


@Parsec
def ParseNumber(state):
    return Number(float("".join(Many1(Digit)(state))))


@Parsec
def ParseBool(state):
    return Bool(Choice(Eq("#f"), Eq("#t"))(state))


@Parsec
def ParseList(state):
    re = List(Between(Eq("(").then(Many(Space)), Many(Space).then(Eq(")")), SepBy(Spaces, ParseExpr))(state))
    return re


@Parsec
def ParseExpr(state):
    return Choice(ParseBool, ParseString, ParseNumber, ParseAtom, ParseList)(state)


@Parsec
def Spaces(state):
    return Many1(Space)(state)


def ReadExpr(expression):
    state = State(expression)
    re = ParseExpr(state)
    return re


#############Standard Library##############
def add(a, *args):
    return a + sum(args)


def sub(a, *args):
    return a - sum(args)


def mul(a, *args):
    return a * reduce(lambda x, y: x * y, args, 1)


def div(a, *args):
    return a / reduce(lambda x, y: x * y, args, 1)


env = Env()
env["+"] = add
env["-"] = sub
env["*"] = mul
env["/"] = div

##################Lab######################


e = EvalVisitor(env)
print e.visit(ReadExpr("(  -  (  + 4  6 3  ) 3 5 2  )"))
print e.visit(ReadExpr("(  -  (  + (  * 2  3 1  )  6 3  ) 3 5 2  )"))
print e.visit(ReadExpr("(if #t 1 2)"))
print e.visit(ReadExpr("(if #f 1 2)"))
# print e.visit(ReadExpr("(define a 1)"))
# print e.visit(ReadExpr("a"))
