# -*-coding:utf8;-*-
import os
import sys


def require(module_path, name=None, root=None, debug=False, force=False):
    """fungsi ini digunakan untuk mengimport file .ly"""
    from Lython.Compiler import lython_compile
    from Lython.Exception import RequireError
    import importlib.util

    if not module_path.endswith(".ly"):
        raise RequireError(module_path + " is not supported file")
    if root is None:
        root = script_path()
    path = os.path.join(root, module_path)

    if not os.path.exists(path):
        raise RequireError(path + " is not exists")
    module_name = os.path.basename(path)[:-3]
    base_dir = os.path.dirname(path)
    module_dir = os.path.join(base_dir, "__lycache__")
    if os.environ.get("LYTHONOPTIMIZE") == "1":
        module_file = os.path.join(module_dir, module_name + ".pyc")
    else:
        module_file = os.path.join(module_dir, module_name + ".py")
    if os.environ.get("LYTHONPRODUCTION") == "1" and not force:
        if not os.path.exists(module_file):
            raise RequireError(module_file + " is not file")
    else:
        if not os.path.exists(module_dir):
            os.makedirs(module_dir)

        lython_compile(path, module_dir, debug)

    if not force:
        spec = importlib.util.spec_from_file_location(module_name, module_file)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = mod
        spec.loader.exec_module(mod)

        if name is not None:
            if not isinstance(name, list):
                raise RequireError("invalid name type")
            names = []
            for i in name:
                names.append(getattr(mod, i))
            if len(names) == 1:
                return names[0]
            else:
                return names
        return mod


def get_require(source_code):
    """
    Mendapatkan argumen dari pemanggilan fungsi dalam kode sumber.

    Parameters:
    source_code (str): Kode sumber yang berisi pemanggilan fungsi.

    Returns:
    dict: Nilai argumen yang dipanggil dalam fungsi.
    """
    import ast

    # Parse the source code into an AST
    tree = ast.parse(source_code)

    # Buat dictionary untuk menyimpan argumen
    args_dict = {}

    # Traverse AST untuk menemukan pemanggilan fungsi
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Dapatkan nama fungsi
            if isinstance(node.func, ast.Name) and node.func.id == "require":
                # Ekstrak argumen
                for arg, arg_name in zip(
                    node.args, ["module_path", "name", "reload", "debug", "force"]
                ):
                    if hasattr(ast, "Constant") and isinstance(
                        arg, ast.Constant
                    ):  # Untuk Python 3.8 ke atas
                        args_dict[arg_name] = arg.value
                    elif isinstance(arg, ast.Str):  # Untuk Python 3.6
                        args_dict[arg_name] = arg.s
                    elif isinstance(arg, ast.Num):  # Untuk Python 3.6
                        args_dict[arg_name] = arg.n
                    elif isinstance(arg, ast.NameConstant):  # Untuk Python 3.6
                        args_dict[arg_name] = arg.value
                    elif isinstance(arg, ast.List):
                        args_dict[arg_name] = [
                            elt.value if hasattr(elt, "value") else elt.s
                            for elt in arg.elts
                        ]
                # Ekstrak keyword arguments
                for keyword in node.keywords:
                    if hasattr(ast, "Constant") and isinstance(
                        keyword.value, ast.Constant
                    ):
                        args_dict[keyword.arg] = keyword.value
                    elif isinstance(keyword.value, ast.Str):
                        args_dict[keyword.arg] = keyword.value.s
                    elif isinstance(keyword.value, ast.Num):
                        args_dict[keyword.arg] = keyword.value.n
                    elif isinstance(keyword.value, ast.NameConstant):
                        args_dict[keyword.arg] = keyword.value.value
                    elif isinstance(keyword.value, ast.List):
                        args_dict[keyword.arg] = [
                            elt.value if hasattr(elt, "value") else elt.s
                            for elt in keyword.value.elts
                        ]
    return args_dict


def find_require(code):
    """
    Menemukan pemanggilan fungsi 'test' dalam kode Python dan mengembalikan
    daftar tuple yang berisi nomor baris dan kode yang memanggil fungsi tersebut.

    Args:
    code (str): Kode Python sebagai string.

    Returns:
    list of tuples: Daftar tuple berisi nomor baris dan kode yang memanggil fungsi 'test'.
    """
    import ast

    # Parse kode menjadi AST
    tree = ast.parse(code)

    # Daftar untuk menyimpan hasil
    results = []

    class RequireCallVisitor(ast.NodeVisitor):
        def visit_Call(self, node):
            # Memeriksa apakah fungsi yang dipanggil bernama 'test'
            if isinstance(node.func, ast.Name) and node.func.id == "require":
                # Mendapatkan kode asli dari node
                line_number = node.lineno
                code_line = code.splitlines()[line_number - 1].strip()
                # Menyimpan hasil ke daftar
                results.append((line_number, code_line))
            # Kunjungi anak node lainnya
            self.generic_visit(node)

    # Inisialisasi dan jalankan visitor
    visitor = RequireCallVisitor()
    visitor.visit(tree)

    return results


def horspool(pattern, text):
    """fungsi ini digunakan mencari posisi kata tertentu"""
    # Step 1: Membuat tabel pergeseran
    m = len(pattern)
    n = len(text)
    shift_table = {char: m for char in set(text)}

    for j in range(m - 1):
        shift_table[pattern[j]] = m - 1 - j

    # Step 2: Pencarian menggunakan tabel pergeseran
    posisi = []
    i = m - 1

    while i < n:
        k = 0
        while k < m and pattern[m - 1 - k] == text[i - k]:
            k += 1
        if k == m:
            posisi.append(i - m + 1)
        i += shift_table.get(text[i], m)

    return posisi


def print_code(code, title="CODE", strip=30):
    """fungsi utilitas untuk mencetak code"""
    lines = strip
    spasi = str(len(code))
    spasi = len(spasi)
    print_code_python = []
    num = 1
    for i in code.split("\n"):
        print_code_python.append(
            " {}{}| {}".format(num, " " * (spasi - len(str(num))), i)
        )
        num = num + 1
    ret = ""
    ret = ret + "\n" + "-" * lines
    ret = ret + "\n" + " " * 5 + title
    ret = ret + "\n" + "-" * lines
    ret = ret + "\n" + "\n".join(print_code_python) + "\n"
    ret = ret + "\n" + "-" * lines
    ret = ret + "\n"
    return ret


def get_vars(source_code):
    """
    Mendapatkan nama variabel yang di-assign dari hasil pemanggilan fungsi dalam kode sumber.

    Parameters:
    source_code (str): Kode sumber yang berisi pemanggilan fungsi.

    Returns:
    list: Nama variabel yang di-assign.
    """
    import ast

    # Parse the source code into an AST
    tree = ast.parse(source_code)

    # List untuk menyimpan nama variabel
    assigned_vars = []

    # Traverse AST untuk menemukan assignment
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            # Periksa target assignment
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned_vars.append(target.id)
                elif isinstance(target, ast.Tuple):
                    for elt in target.elts:
                        if isinstance(elt, ast.Name):
                            assigned_vars.append(elt.id)
    return assigned_vars


def touch(path):
    """
    Membuat file baru jika belum ada, atau memperbarui timestamp jika sudah ada.

    Parameters:
    path (str): Path dari file yang akan dibuat atau diperbarui.
    """
    # Cek apakah file sudah ada
    if os.path.exists(path):
        # Perbarui timestamp
        os.utime(path, None)
    else:
        # Buat file baru
        open(path, "a").close()


def read(path):
    """fungsi untuk membaca file"""
    with open(path, "r") as f:
        ret = f.read()
    return ret


def write(path, code):
    """fungsi untuk menulis file"""
    with open(path, "w") as f:
        f.write(code)


def print_e(content):
    """fungsi untuk print pada std.err"""
    print(content, file=sys.stderr)
    exit(1)


def script_path():
    """mendapatkan lokasi script path"""
    p = os.environ.get("LYTHON_FILE", sys.argv[0])
    return os.path.abspath(os.path.dirname(p))
