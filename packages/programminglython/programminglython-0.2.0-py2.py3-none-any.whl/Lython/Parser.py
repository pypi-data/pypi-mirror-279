# -*-coding:utf8;-*-
from io import StringIO
import re
import tokenize
from Lython.util import horspool
import os
import traceback
from Lython.Exception import ParseError
import ast


error_msg = """
  File "{}", line {}
    {}
   {}^
{}
"""
error_msg = error_msg.strip()


def python_syntax_checker(code, filename="<str>"):
    """fungsi untuk memverifikasi python syntax"""
    try:
        cx = compile(code, filename=filename, mode="exec")
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
        raise ParseError(err)
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
        raise ParseError(err)


def lython_syntax_checker(code, filename="<str>"):
    """fungsi untuk mencegah daftar keywords digunakan sebagai nama variabel, function dan class"""
    keywords = ("do", "end", "then")
    toks = tokenize.generate_tokens(StringIO(code).readline)
    for toktype, tokvalue, baris, _, code in toks:
        baris = baris[0]

        if toktype == tokenize.NAME and tokvalue in keywords:
            code = code.strip()
            if tokvalue == "end":
                lok = horspool("end", code)[0]
            elif tokvalue == "do":
                lok = horspool("do", code)[0]
            else:
                lok = horspool("then", code)[0]
            raise ParseError(
                error_msg.format(
                    filename,
                    baris,
                    code,
                    " " * (lok + 1),
                    "SyntaxError: invalid syntax",
                )
            )


def inline_syntax_checker(lycode, code, line, filename):
    """fungsi syntax check tambahan untuk repl"""
    codes = code.strip()
    if not codes.endswith(" pass"):
        codes = codes + " pass"
    try:
        ast.parse(codes)
    except SyntaxError as e:
        file_path = filename
        line_number = line
        error_line = lycode
        indicator_line = "{:>{}}".format("^", e.offset)

        err = 'File "{}", line {}\n    {}\n    {}'.format(
            file_path, line_number, error_line, indicator_line
        )
        err = err + "\n" + "{}: {}".format(type(e).__name__, e.msg)
        raise ParseError(err)
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        last_tb = tb[-1]
        error_details = traceback.format_exception_only(type(e), e)[-1].strip()
        error_line = lycode
        err = 'File "{}", line {}\n    {}'.format(filename, line, error_line)
        err = err + "\n" + error_details
        raise ParseError(err)
    lython_syntax_checker(code, filename)


def ignore_comments(code):
    """fungsi untuk mengabaikan komentar saat parsing"""
    r = re.sub(r"\#.*", "", code)
    return r.strip()


def parse(code, filename="<str>"):
    """fungsi untuk memparse Lython syntax menjadi normal Python syntax"""
    mode_doc_string_double_quote = False
    mode_doc_string_single_quote = False
    lines = code.splitlines()
    new_lines = []
    indent_level = 0
    indent = "    "  # Empat spasi untuk indentasi
    block = ("class ", "def ")  # block tanpa identifier
    block_then = ("if ",)
    block_do = ("while ", "for ", "with ")
    all_block = ("try:", "except:", "else:")
    all_block_arg = (
        "if ",
        "elif ",
        "except ",
        "def ",
        "async def ",
        "with ",
        "async with ",
        "for ",
        "while ",
        "class ",
    )

    lineno = 1
    block_open = []
    block_close = []
    for line in lines:
        stripped = line.strip()
        # implementasi doc string double quote
        if stripped == '"""' or re.match(r'^\w+\s*=\s*"""$', stripped):
            if not mode_doc_string_single_quote:
                if not mode_doc_string_double_quote:
                    mode_doc_string_double_quote = True
                else:
                    mode_doc_string_double_quote = False
        # implementasi doc string single quote
        elif stripped == "'''" or re.match(r"^\w+\s*=\s*'''$", stripped):
            if not mode_doc_string_double_quote:
                if not mode_doc_string_single_quote:
                    mode_doc_string_single_quote = True
                else:
                    mode_doc_string_single_quote = False
        if mode_doc_string_double_quote or mode_doc_string_single_quote:
            new_lines.append(indent * indent_level + stripped)
        else:
            # raise error old python ":"
            if stripped.endswith(":"):
                raise ParseError(
                    error_msg.format(
                        filename,
                        lineno,
                        stripped,
                        " " * len(stripped),
                        "SyntaxError: invalid syntax",
                    )
                )
            # implementasi try
            elif stripped == "try":
                new_lines.append(indent * indent_level + stripped + ":")
                indent_level += 1
                block_open.append((stripped, lineno))
            # implementasi block
            elif stripped.startswith(block):
                if stripped.endswith(" pass"):
                    gencode = stripped[:-5]
                    gencode = indent * indent_level + gencode + ":" + " pass"
                else:
                    gencode = indent * indent_level + stripped + ":"
                    indent_level += 1
                new_lines.append(gencode)
                block_open.append((stripped, lineno))

            # implementasi async def
            elif stripped.startswith("async def "):
                if stripped.endswith(" pass"):
                    gencode = stripped[:-5]
                    gencode = indent * indent_level + gencode + ":" + " pass"
                else:
                    gencode = indent * indent_level + stripped + ":"
                    indent_level += 1
                new_lines.append(gencode)
                block_open.append((stripped, lineno))

            # implementasi block then
            elif stripped.startswith(block_then):
                if stripped.endswith(" then"):
                    new_lines.append(indent * indent_level + stripped[:-5] + ":")
                    indent_level += 1
                    block_open.append((stripped, lineno))
                else:
                    raise ParseError(
                        error_msg.format(
                            filename,
                            lineno,
                            stripped,
                            " " * (len(stripped) + 2),
                            "SyntaxError: expected an 'then' keyword",
                        )
                    )
            # implementasi block do
            elif stripped.startswith(block_do):
                if stripped.endswith(" do"):

                    new_lines.append(indent * indent_level + stripped[:-3] + ":")
                    indent_level += 1
                    block_open.append((stripped, lineno))
                else:
                    raise ParseError(
                        error_msg.format(
                            filename,
                            lineno,
                            stripped,
                            " " * (len(stripped) + 2),
                            "SyntaxError: expected an 'do' keyword",
                        )
                    )
            # implementasi async with
            elif stripped.startswith("async with "):
                if stripped.endswith(" do"):

                    new_lines.append(indent * indent_level + stripped[:-3] + ":")
                    indent_level += 1
                    block_open.append((stripped, lineno))
                else:
                    raise ParseError(
                        error_msg.format(
                            filename,
                            lineno,
                            stripped,
                            " " * 2,
                            "expected an 'do' keyword",
                        )
                    )
            # implementasi elif
            elif stripped.startswith("elif "):
                if stripped.endswith(" then"):

                    indent_level -= 1
                    new_lines.append(indent * indent_level + stripped[:-5] + ":")
                    indent_level += 1
                else:
                    raise ParseError(
                        error_msg.format(
                            filename,
                            lineno,
                            stripped,
                            " " * (len(stripped) + 2),
                            "SyntaxError: expected an 'then' keyword",
                        )
                    )
            # implementasi match
            elif stripped.startswith("match "):
                new_lines.append(indent * indent_level + stripped + ":")
                indent_level += 1
                block_open.append((stripped, lineno))
            # implementasi case
            elif stripped.startswith("case "):
                if stripped.endswith(" do"):
                    new_lines.append(indent * indent_level + stripped[:-3] + ":")
                    indent_level += 1
                    block_open.append((stripped, lineno))
                else:
                    raise ParseError(
                        error_msg.format(
                            filename,
                            lineno,
                            stripped,
                            " " * (len(stripped) + 2),
                            "SyntaxError: expected an 'do' keyword",
                        )
                    )
            # implementasi except dengan argument
            elif stripped.startswith("except "):
                if stripped.endswith(" do"):

                    indent_level -= 1
                    new_lines.append(indent * indent_level + stripped[:-3] + ":")
                    indent_level += 1
                else:
                    raise ParseError(
                        error_msg.format(
                            filename,
                            lineno,
                            stripped,
                            " " * 2,
                            "expected an 'do' keyword",
                        )
                    )
            # implementasi end keyword
            elif ignore_comments(stripped) == "end":
                if len(new_lines):
                    e_stripped = new_lines[-1].strip()
                    if e_stripped.startswith(all_block_arg) or e_stripped in all_block:
                        raise ParseError(
                            error_msg.format(
                                filename,
                                lineno,
                                stripped,
                                " " * 2,
                                "SyntaxError: Can't 'end' empty block",
                            )
                        )

                if indent_level > 0:
                    indent_level -= 1
                    block_close.append(stripped)
                    new_lines.append(indent * indent_level + "# " + stripped)
                else:
                    raise ParseError(
                        error_msg.format(
                            filename,
                            lineno,
                            stripped,
                            " " * 2,
                            "SyntaxError: unexpected 'end'",
                        )
                    )
            # implementasi else dan except
            elif stripped == "else" or stripped == "except":
                indent_level -= 1
                new_lines.append(indent * indent_level + stripped + ":")
                indent_level += 1
            else:
                new_lines.append(indent * indent_level + stripped)
        lineno = lineno + 1
    # trigger error untuk block yang belum ditutup
    if len(block_open) != len(block_close):
        raise ParseError(
            error_msg.format(
                filename,
                block_open[-1][1],
                block_open[-1][0],
                " " * 2,
                "SyntaxError: 'end' expected",
            )
        )

    final_code = "\n".join(new_lines)
    python_syntax_checker(final_code, filename)
    lython_syntax_checker(final_code, filename)
    return final_code


def repl_parse(
    code,
    new_lines=[],
    block_open=[],
    block_close=[],
    filename="<console>",
    indent_level=0,
    lineno=1,
    mode_doc_string_double_quote=False,
    mode_doc_string_single_quote=False,
):
    """fungsi parse yang digunakan pada repl"""

    indent = "    "  # Empat spasi untuk indentasi
    block = ("class ", "def ")  # block tanpa identifier
    block_then = ("if ",)
    block_do = ("while ", "for ", "with ")
    ret_code = ""
    skip = True
    all_block = ("try:", "except:", "else:")
    all_block_arg = (
        "if ",
        "elif ",
        "except ",
        "def ",
        "async def ",
        "with ",
        "async with ",
        "for ",
        "while ",
        "class ",
    )

    stripped = code.strip()
    # implementasi doc string double quote
    if stripped == '"""' or re.match(r'^\w+\s*=\s*"""$', stripped):
        if not mode_doc_string_single_quote:
            if not mode_doc_string_double_quote:
                mode_doc_string_double_quote = True
            else:
                mode_doc_string_double_quote = False
    # implementasi doc string single quote
    elif stripped == "'''" or re.match(r"^\w+\s*=\s*'''$", stripped):
        if not mode_doc_string_double_quote:
            if not mode_doc_string_single_quote:
                mode_doc_string_single_quote = True
            else:
                mode_doc_string_single_quote = False
    if mode_doc_string_double_quote or mode_doc_string_single_quote:
        ret_code = indent * indent_level + stripped
        new_lines.append(indent * indent_level + stripped)
    else:
        # raise error old python ":"
        if stripped.endswith(":"):
            raise ParseError(
                error_msg.format(
                    filename,
                    lineno,
                    stripped,
                    " " * len(stripped),
                    "SyntaxError: invalid syntax",
                )
            )
        # implementasi try
        elif stripped == "try":
            new_lines.append(indent * indent_level + stripped + ":")
            ret_code = indent * indent_level + stripped + ":"
            indent_level += 1
            block_open.append((stripped, lineno))
        # implementasi block
        elif stripped.startswith(block):
            if stripped.endswith(" pass"):
                gencode = stripped[:-5]
                gencode = indent * indent_level + gencode + ":" + " pass\n"
            else:
                gencode = indent * indent_level + stripped + ":"
                indent_level += 1
            new_lines.append(gencode)
            block_open.append((stripped, lineno))
            inline_syntax_checker(stripped, gencode, lineno, filename)
            ret_code = gencode
        # implementasi async def
        elif stripped.startswith("async def "):
            if stripped.endswith(" pass"):
                gencode = stripped[:-5]
                gencode = indent * indent_level + gencode + ":" + " pass\n"
            else:
                gencode = indent * indent_level + stripped + ":"
                indent_level += 1
            new_lines.append(gencode)
            block_open.append((stripped, lineno))
            inline_syntax_checker(stripped, gencode, lineno, filename)
            ret_code = gencode
        # implementasi block then
        elif stripped.startswith(block_then):
            if stripped.endswith(" then"):
                ret_code = indent * indent_level + stripped[:-5] + ":"
                new_lines.append(indent * indent_level + stripped[:-5] + ":")
                indent_level += 1
                block_open.append((stripped, lineno))
            else:
                raise ParseError(
                    error_msg.format(
                        filename,
                        lineno,
                        stripped,
                        " " * (len(stripped) + 2),
                        "SyntaxError: expected an 'then' keyword",
                    )
                )
        # implementasi block do
        elif stripped.startswith(block_do):
            if stripped.endswith(" do"):

                new_lines.append(indent * indent_level + stripped[:-3] + ":")
                ret_code = indent * indent_level + stripped[:-3] + ":"
                indent_level += 1
                block_open.append((stripped, lineno))
            else:
                raise ParseError(
                    error_msg.format(
                        filename,
                        lineno,
                        stripped,
                        " " * (len(stripped) + 2),
                        "SyntaxError: expected an 'do' keyword",
                    )
                )
        # implementasi async with
        elif stripped.startswith("async with "):
            if stripped.endswith(" do"):

                new_lines.append(indent * indent_level + stripped[:-3] + ":")
                ret_code = indent * indent_level + stripped[:-3] + ":"
                indent_level += 1
                block_open.append((stripped, lineno))
            else:
                raise ParseError(
                    error_msg.format(
                        filename, lineno, stripped, " " * 2, "expected an 'do' keyword"
                    )
                )
        # implementasi elif
        elif stripped.startswith("elif "):
            if stripped.endswith(" then"):

                indent_level -= 1
                new_lines.append(indent * indent_level + stripped[:-5] + ":")
                ret_code = indent * indent_level + stripped[:-5] + ":"
                indent_level += 1
            else:
                raise ParseError(
                    error_msg.format(
                        filename,
                        lineno,
                        stripped,
                        " " * (len(stripped) + 2),
                        "SyntaxError: expected an 'then' keyword",
                    )
                )
        # implementasi match
        elif stripped.startswith("match "):
            new_lines.append(indent * indent_level + stripped + ":")
            ret_code = indent * indent_level + stripped + ":"
            indent_level += 1
            block_open.append((stripped, lineno))
        # implementasi case
        elif stripped.startswith("case "):
            if stripped.endswith(" do"):
                new_lines.append(indent * indent_level + stripped[:-3] + ":")
                ret_code = indent * indent_level + stripped[:-3] + ":"
                indent_level += 1
                block_open.append((stripped, lineno))
            else:
                raise ParseError(
                    error_msg.format(
                        filename,
                        lineno,
                        stripped,
                        " " * (len(stripped) + 2),
                        "SyntaxError: expected an 'do' keyword",
                    )
                )
        # implementasi except dengan argument
        elif stripped.startswith("except "):
            if stripped.endswith(" do"):

                indent_level -= 1
                new_lines.append(indent * indent_level + stripped[:-3] + ":")
                ret_code = indent * indent_level + stripped[:-3] + ":"
                indent_level += 1
            else:
                raise ParseError(
                    error_msg.format(
                        filename, lineno, stripped, " " * 2, "expected an 'do' keyword"
                    )
                )
        # implementasi end keyword
        elif ignore_comments(stripped) == "end":
            if len(new_lines):
                e_stripped = new_lines[-1].strip()
                if e_stripped.startswith(all_block_arg) or e_stripped in all_block:
                    raise ParseError(
                        error_msg.format(
                            filename,
                            lineno,
                            stripped,
                            " " * 2,
                            "SyntaxError: Can't 'end' empty block",
                        )
                    )

            if indent_level > 0:
                skip = True
                indent_level -= 1
                block_close.append(stripped)
                new_lines.append(indent * indent_level + "# " + stripped)
                ret_code = indent * indent_level
            else:
                raise ParseError(
                    error_msg.format(
                        filename,
                        lineno,
                        stripped,
                        " " * 2,
                        "SyntaxError: unexpected 'end'",
                    )
                )
        # implementasi else dan except
        elif stripped == "else" or stripped == "except":
            indent_level -= 1
            new_lines.append(indent * indent_level + stripped + ":")
            indent_level += 1
        else:
            ret_code = indent * indent_level + stripped
            skip = False
        lineno = lineno + 1
    if not skip:
        lython_syntax_checker(code, filename)
    return (
        ret_code,
        new_lines,
        block_open,
        block_close,
        indent_level,
        lineno,
        mode_doc_string_double_quote,
        mode_doc_string_single_quote,
    )
