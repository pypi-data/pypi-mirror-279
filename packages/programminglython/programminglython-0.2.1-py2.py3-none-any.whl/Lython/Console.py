# -*-coding:utf8;-*-
from Lython.util import print_code, print_e, read, write, require
from Lython.Parser import parse
from Lython.Repl import LythonInteractiveShell
from Lython.Interpreter import python, lython
from Lython.Compiler import lython_compile
import os
import sys
import argparse


if os.environ.get("LYTHONOPTIMIZE") is None:
    os.environ["LYTHONOPTIMIZE"] = "1"


def lint(source):
    """fungsi untuk memvalidasi sintaks"""

    try:
        code = read(source)
        lython_code = parse(code)
        print("No syntax errors detected in", source)
    except BaseException as e:
        print_e(e)


def repl():
    """fungsi untuk  menjalankan repl"""

    sys.argv[0] = os.path.join(os.getcwd(), "__repl__.ly")
    lython_shell = LythonInteractiveShell()
    lython_shell.interact()
    return


def interpreter(source, argv, debug=False):
    """fungsi untuk menjalankan interpreter"""

    if debug:
        print("[debug] LYTHONPRODUCTION =", os.environ.get("LYTHONPRODUCTION"))
        print("[debug] LYTHONOPTIMIZE =", os.environ.get("LYTHONOPTIMIZE"))
    argv = [source] + argv
    sys.argv = argv
    if os.environ.get("LYTHONOPTIMIZE") == "1":
        try:
            ret = python(source, sys.argv, debug=debug)
            if ret != 0:
                exit(ret)

        except BaseException as e:
            print_e(e)
    else:
        # this interpreter only for dev lython
        parse_error = False
        code = read(source)
        sandbox = {}
        pyast = lython(code, filename=source)
        exec(pyast, sandbox, sandbox)
        sandbox = {}


def show(source):
    """fungsi untuk menjalankan print_code"""

    try:
        code = read(source)
        lython_code = parse(code, filename=source)
        print(print_code(code, "PYTHON CODE"))
        print(print_code(lython_code, "LYTHON CODE"))
    except BaseException as e:
        print_e(e)


def _compile(source):
    """fungsi untuk menjalankan compile"""
    print("\nENTRYPOINT:\n")
    print("compiling:", source)
    try:
        lython_compile(source)
    except BaseException as e:
        print_e(e)
    print("\n__LYCACHE__:\n")
    entrypoint = os.path.abspath(source)
    path = os.path.dirname(entrypoint)
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith(".ly"):
                file_path = os.path.join(root, file_name)
                if file_path != entrypoint:
                    print("compiling: {}".format(file_path))
                    try:
                        require(file_path, force=True)
                    except BaseException as e:
                        print_e(e)


def main():
    """fungsi utama saat dipanggil langsung"""
    parser = argparse.ArgumentParser(
        description="Lython programming language built on top of CPython"
    )
    parser.add_argument("path", nargs="?", type=str, help="The path to the .ly file")
    parser.add_argument("-d", "--debug", action="store_true", help="Debug mode")
    parser.add_argument(
        "-c",
        "--compile",
        action="store_true",
        help="Compile your Lython project for deployment",
    )
    parser.add_argument("-l", "--lint", action="store_true", help="Syntax check only")
    parser.add_argument(
        "-p", "--print", action="store_true", help="Print the code only"
    )
    parser.add_argument(
        "-V", "--version", action="store_true", help="Show Lython version"
    )

    args, argv = parser.parse_known_args()

    if args.path is None:
        if args.version:
            import Lython

            print("Lython", Lython.__version__, "by guangrei")
            return
        return repl()

    if not os.path.isfile(args.path):
        print_e("error: can't open file '{}'".format(args.path))

    if not args.path.endswith(".ly"):
        print_e("error: unsupported file '{}'".format(args.path))

    if args.print:
        show(args.path)

    elif args.compile:
        _compile(args.path)

    elif args.lint:
        lint(args.path)
    else:
        interpreter(args.path, argv=argv, debug=args.debug)


if __name__ == "__main__":
    main()
