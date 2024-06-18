# -*-coding:utf8;-*-
import sys
import traceback
import code
from Lython.Parser import repl_parse, parse, ignore_comments
from Lython.util import require
from var_dump import var_dump
from pprint import pprint


class LythonInteractiveShell(code.InteractiveConsole):
    """class LythonInteractiveShell untuk menjalankan repl"""

    def __init__(self, locals=None, filename="<console>", histfile=None):
        super().__init__(locals=locals, filename=filename)
        self.locals["require"] = require
        self.locals["var_dump"] = var_dump
        self.locals["pprint"] = pprint
        self.locals["dump"] = self.dump
        self._new_lines = []
        self._block_open = []
        self._block_close = []
        self._indent_level = 0
        self._lineno = 1
        self._mode_doc_string_double_quote = False
        self._mode_doc_string_single_quote = False

    def dump(self, variable):
        """fungsi dump untuk memudahkan debug"""
        from inspect import getmembers

        pprint(getmembers(variable))

    def raw_input(self, prompt=None):
        """fungsi untuk menghandle input pada repl"""
        if hasattr(sys, "last_type") and not sys.last_type == "":
            self._new_lines = []
            self._block_open = []
            self._block_close = []
            self._indent_level = 0
            self._lineno = 1
            self._mode_doc_string_double_quote = False
            self._mode_doc_string_single_quote = False
            sys.last_type = ""
            self.resetbuffer()

        if self._indent_level != 0:
            prompt = "... "
        else:
            prompt = ">>> "
            self._lineno = 1
            self._indent_level = 0
        return input(prompt)

    def push(self, line):
        """fungsi untuk memparse code yang di input"""

        try:
            (
                parsed,
                self._new_lines,
                self._block_open,
                self._block_close,
                self._indent_level,
                self._lineno,
                self._mode_doc_string_double_quote,
                self._mode_doc_string_single_quote,
            ) = repl_parse(
                line,
                new_lines=self._new_lines,
                block_open=self._block_open,
                block_close=self._block_close,
                indent_level=self._indent_level,
                lineno=self._lineno,
                mode_doc_string_double_quote=self._mode_doc_string_double_quote,
                mode_doc_string_single_quote=self._mode_doc_string_single_quote,
            )
            if ignore_comments(parsed) == "end" and self._indent_level == 1:
                parsed = parsed + "\n"
        except BaseException as e:
            sys.stderr.write(str(e) + "\n")
            self._new_lines = []
            self._block_open = []
            self._block_close = []
            self._indent_level = 0
            self._lineno = 1
            self._mode_doc_string_double_quote = False
            self._mode_doc_string_single_quote = False
            self.resetbuffer()
            parsed = "\n"
        go = super().push(parsed)
        return go
