# -*-coding:utf8;-*-
from Lython.Parser import parse
import py_compile
import traceback
import sys
import os
from Lython.Exception import CompileError
from Lython import util


def lython_compile(source, dist_dir=None, debug=False):
    """fungsi parent untuk mengcompile .ly menjadi .pyc"""
    if not source.endswith(".ly"):
        raise CompileError(source + " is not supported")
    if not os.path.isfile(source):
        raise CompileError(source + "is not file")
    base_file = os.path.basename(source)[:-3]
    base_dir = os.path.dirname(source)
    if dist_dir is None:
        dist_dir = base_dir
    if os.environ.get("LYTHONOPTIMIZE") == "1":
        dist_file = os.path.join(dist_dir, base_file + ".pyc")
    else:
        dist_file = os.path.join(dist_dir, base_file + ".py")
    if os.path.isfile(dist_file):
        if _isRecompileAble(source, dist_file):
            if debug:
                print("[compiler] compiling:", source, "to", dist_file)
            if os.environ.get("LYTHONOPTIMIZE") == "1":
                ly2pyc(source, dist_file, base_dir)
            else:
                ly2py(source, dist_file)
        else:
            if debug:
                print("[compiler] no need to compile:", source)
    else:
        if debug:
            print("[compiler] compiling:", source, "to", dist_file)
        if os.environ.get("LYTHONOPTIMIZE") == "1":
            ly2pyc(source, dist_file, base_dir)
        else:
            ly2py(source, dist_file)
    return dist_file


def _isRecompileAble(source_file, compiled_file):
    """fungsi untuk mengecek apakah source_file perlu di compile ulang"""
    source_mtime = os.path.getmtime(source_file)
    compiled_mtime = os.path.getmtime(compiled_file)
    return source_mtime > compiled_mtime


def ly2py(source, target):
    """fungsi untuk mengcompile .ly ke .py"""
    basefile = os.path.basename(source)[:-3]
    code = util.read(source)
    code = parse(code, filename=source)
    util.write(target, code)


def ly2pyc(source, target, source_dir):
    """fungsi untuk mengcompile .ly ke .pyc"""
    basefile = os.path.basename(source)[:-3]
    code = util.read(source)
    # tmp py file for compile
    fname = os.path.join(source_dir, basefile + ".tmp_py")
    code = parse(code, filename=source)
    util.write(fname, code)
    try:
        py_compile.compile(fname, cfile=target)
    except SyntaxError as e:
        # Menangani SyntaxError secara khusus
        file_path = e.filename
        line_number = e.lineno
        error_line = e.text.strip()
        indicator_line = "{:>{}}".format("^", e.offset)

        err = 'File "{}", line {}\n    {}\n    {}'.format(
            file_path, line_number, error_line, indicator_line
        )
        err = err + "\n" + "{}: {}".format(type(e).__name__, e.msg)
        raise CompileError(err)
    except Exception as e:
        # Menangani Exception lain
        tb = traceback.extract_tb(e.__traceback__)
        last_tb = tb[-1]
        error_details = traceback.format_exception_only(type(e), e)[-1].strip()
        error_line = code.split("\n")[last_tb.lineno - 1]

        err = 'File "{}", line {}\n    {}'.format(
            last_tb.filename, last_tb.lineno, error_line
        )
        err = err + "\n" + error_details
        raise CompileError(err)
    os.remove(fname)


def ly2native(source, parent_dir=None):
    """
    fungsi untuk mengconvert code lython menjadi native python
    note: fungsi ini belum sempurna
    """
    code = util.read(source)
    code = parse(code)
    codelines = code.split("\n")
    task = util.find_require(code)
    for i in task:
        a = i[0] - 1
        c = i[1]
        indent = codelines[a].split(codelines[a].strip())[0]
        r = util.get_require(c)
        modfile = r["module_file"]
        if parent_dir is not None:
            modfile = modfile.replace(parent_dir, "")
        base_file = os.path.basename(modfile)[:-3]
        moddir = base_file
        base_dir = os.path.dirname(modfile)
        if len(base_dir):
            moddir = os.path.split(base_dir)
            if len(moddir) == 1:
                moddir = moddir[0]
            else:
                moddir = ".".join(moddir)
            moddir = moddir + "." + base_file
            moddir = moddir.replace("\\", "")
            moddir = moddir.replace("/", "")

        if len(r):
            v = util.get_vars(c)
            if len(v) == 1:
                if v[0] != base_file and "name" not in r:
                    codelines[a] = indent + "import {} as {}".format(moddir, v[0])
                elif v[0] != base_file and "name" in r:
                    codelines[a] = indent + "from {} import {} as {}".format(
                        moddir, r["name"][0], v[0]
                    )
                elif v[0] == base_file and "name" in r:
                    codelines[a] = indent + "from {} import {}".format(
                        moddir, r["name"][0]
                    )
                else:
                    codelines[a] = indent + "import {} as {}".format(moddir, base_file)
            else:
                if "name" in r:
                    codelines[a] = indent + "from {} import {}".format(
                        moddir, ", ".join(r["name"])
                    )
                else:
                    codelines[a] = indent + "import {} as {}".format(moddir, base_file)
    n = 0
    for i in codelines:
        if i.strip() == "from Lython.util import require":
            del codelines[n]
        n = n + 1
    return "\n".join(codelines).strip()
