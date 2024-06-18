# -*-coding:utf8;-*-
from pathlib import Path
import platform
import tempfile
import sys
import os
import traceback
from Lython.Compiler import lython_compile
from Lython.Parser import parse
from Lython.Exception import InterpreterError


def python(file, argv, debug=False):
    """interpreter dengan sys.executable"""
    py = sys.executable
    if not file.endswith(".ly"):
        raise InterpreterError(file + " is not supported")
    if not os.path.isfile(file):
        raise InterpreterError(file + " is not file")
    base_dir = os.path.dirname(os.path.abspath(file))
    base_file = os.path.basename(file)[:-3]
    tempdir = Path("/tmp" if platform.system() == "Darwin" else tempfile.gettempdir())
    cachedir = os.path.join(tempdir, ".lython")
    cachedir = os.path.join(cachedir, "__lycache__" + base_dir)
    path = Path(cachedir)
    path.mkdir(parents=True, exist_ok=True)
    pyc = lython_compile(file, cachedir, debug=debug)
    if debug:
        print("[debug] Run file:", pyc)
    argv[0] = pyc
    argv.insert(0, py)
    os.environ["LYTHON_FILE"] = os.path.abspath(file)
    ret = os.system(" ".join(argv))
    return ret


def lython(code, filename="<str>"):
    """interpreter dengan exec"""
    from Lython.ClassParser import ClassParser
    import ast

    pycode = parse(code, filename)
    parsed_ast = ast.parse(pycode)
    parser = ClassParser()
    _ast = parser.visit(parsed_ast)
    py = compile(_ast, filename=filename, mode="exec")
    return py
