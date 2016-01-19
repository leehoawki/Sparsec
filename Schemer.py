from Sparsec import *


###########Types and Builtin###############

class Env(dict):
    def __init__(self, parent=None):
        self.parent = parent

    def get(self, k, d=None):
        re = super(Env, self).get(k, d)
        if re is not None:
            return re
        if self.parent is not None:
            return self.parent.get(k, d)
        return None


env = Env()


class Ast(object):
    def __init__(self, val):
        self.val = val

    def accept(self, visitor):
        pass


class Bool(Ast):
    a = {"#t": True, "#f": False}

    def __init__(self, val):
        self.val = self.__class__.a.get(val)

    def accept(self, visitor):
        return visitor.visit(self)


class Number(Ast):
    def accept(self, visitor):
        return visitor.visit(self)


class String(Ast):
    def accept(self, visitor):
        return visitor.visit(self)


class List(Ast):
    def accept(self, visitor):
        return visitor.visit(self)


class Atom(Ast):
    def accept(self, visitor):
        return visitor.visit(self)


#############Eval and Apply################

class Visitor(object):
    def visit(self, visited):
        return getattr(self, "visit%s" % visited.__class__.__name__)(visited)


class EvalVisitor(Visitor):
    def visitString(self, visited):
        return visited.val

    def visitNumber(self, visited):
        return visited.val

    def visitAtom(self, visited):
        return env.get(visited.val)

    def visitList(self, visited):
        func = visited.val[0].accept(self)
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
    return Atom("".join(Many1(Alphabet)(state)))


@Parsec
def ParseNumber(state):
    return Number(float("".join(Many1(Digit)(state))))


@Parsec
def ParseBool(state):
    return Bool(Choice(Eq("#f"), Eq("#t"))(state))


@Parsec
def ParseList(state):
    return List(Between(Eq("("), Eq(")"), SepBy(" ", ParseExpr))(state))


@Parsec
def ParseExpr(state):
    return Choice(ParseBool, ParseString, ParseNumber, ParseAtom, ParseList)(state)


def ReadExpr(expression):
    state = State(expression)
    re = ParseExpr(state)
    return re


#############Standard Library##############
def add(a, *args):
    return a + sum(args)


env["add"] = add

##################Lab######################


print EvalVisitor().visit(ReadExpr('(add 1 2)'))
