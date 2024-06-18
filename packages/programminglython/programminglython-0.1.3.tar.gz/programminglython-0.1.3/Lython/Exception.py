# -*-coding:utf8;-*-


class ParseError(RuntimeError):
    pass


class CompileError(RuntimeError):
    pass


class InterpreterError(RuntimeError):
    pass


class RequireError(RuntimeError):
    pass
