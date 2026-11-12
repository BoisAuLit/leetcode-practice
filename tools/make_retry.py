#!/usr/bin/env python3
"""
make_retry.py — 把 solution.py 变成闭卷重写用的 solution_retry.py

规则：
  1. 所有 class 里的所有方法（含 __init__、被装饰的、async 的）的函数体整个换成一行 `pass`；
     class 范围内的所有 # 注释（方法体里、def 行尾、方法之间）一并删掉，不留任何提示；
  2. 清空之后没人用的 import 一并删掉（不剧透该用什么工具，例如 lru_cache / deque）；
     部分用到的 from-import 只保留用到的名字；`from __future__` 永远保留；
  3. 文件开头加上题目链接注释（从同目录 metadata.json 的 link 读，有几个放几个）；
  4. 其他一切（注释、类外的顶层代码、方法签名、装饰器、空行）原封不动。

用法：
    python3 tools/make_retry.py <题目文件夹或 solution.py>   在同目录写出 solution_retry.py
    python3 tools/make_retry.py --stdout <solution.py>        只打印，不写文件
也被 review_due.py shuffle 直接 import 调用。
"""
from __future__ import annotations
import ast, json, sys
from pathlib import Path

RETRY_NAME = "solution_retry.py"


def _method_ranges(tree: ast.AST) -> list[tuple[int, int, int, int]]:
    """返回每个 class 直接方法的 (def_lineno, body_first_lineno, body_first_col, end_lineno)。
    嵌套在别的方法体里的 class/方法不单独处理（外层方法体被整个替换时它们一起消失）。"""
    ranges = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for fn in node.body:
            if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) and fn.body:
                first = fn.body[0]
                # 方法体第一句如果是带装饰器的嵌套函数/类，lineno 指向 def 行而不是装饰器行，
                # 要从装饰器那一行开始替换，否则 @lru_cache 会被单独留下来变成语法错误
                decos = getattr(first, "decorator_list", None) or []
                first_ln = min([first.lineno] + [d.lineno for d in decos])
                ranges.append((fn.lineno, first_ln, first.col_offset, fn.end_lineno))
    # 去掉被别的范围包含的（嵌套在方法体内的 class 的方法）
    out = []
    for r in ranges:
        if not any(o is not r and o[0] <= r[0] and r[3] <= o[3] and (o[0], o[3]) != (r[0], r[3]) for o in ranges):
            out.append(r)
    return sorted(out, key=lambda r: r[1], reverse=True)   # 从后往前改，行号不会互相影响


def _strip_class_comments(src: str) -> str:
    """删掉所有 class 范围内的 # 注释（方法体里的、def 行尾的、方法之间的），只剩 pass 不剩提示。
    class 之外（import、顶层测试代码）的注释不动。用 tokenize 判断，字符串里的 # 不会误删。"""
    import io, tokenize
    tree = ast.parse(src)
    ranges = [(n.lineno, n.end_lineno) for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    if not ranges:
        return src
    lines = src.splitlines(keepends=True)
    cuts: dict[int, int] = {}                      # 行号 → 注释开始的列
    try:
        for t in tokenize.generate_tokens(io.StringIO(src).readline):
            if t.type == tokenize.COMMENT and any(a <= t.start[0] <= b for a, b in ranges):
                cuts[t.start[0]] = min(cuts.get(t.start[0], t.start[1]), t.start[1])
    except (tokenize.TokenError, IndentationError):
        return src
    out = []
    for i, line in enumerate(lines, start=1):
        if i in cuts:
            kept = line[:cuts[i]].rstrip()
            if not kept:
                continue                            # 整行都是注释 → 整行删掉
            line = kept + ("\n" if line.endswith("\n") else "")
        out.append(line)
    return "".join(out)


def stub_methods(src: str) -> str:
    src = _strip_class_comments(src)
    tree = ast.parse(src)
    lines = src.splitlines(keepends=True)
    for def_ln, body_ln, body_col, end_ln in _method_ranges(tree):
        if body_ln == def_ln:
            # 单行方法 `def f(self): return 1` → 冒号后面换成 pass
            line = lines[def_ln - 1]
            nl = "\n" if line.endswith("\n") else ""
            lines[def_ln - 1:end_ln] = [line[:body_col] + "pass" + nl]
        else:
            first = lines[body_ln - 1]
            indent = first[: len(first) - len(first.lstrip())]
            nl = "\n" if lines[end_ln - 1].endswith("\n") or end_ln < len(lines) else ""
            lines[body_ln - 1:end_ln] = [indent + "pass" + nl]
    return "".join(lines)


def _used_names(tree: ast.AST) -> set[str]:
    used = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.Attribute):
            base = node
            while isinstance(base, ast.Attribute):
                base = base.value
            if isinstance(base, ast.Name):
                used.add(base.id)
    return used


def strip_unused_imports(src: str) -> str:
    """删掉顶层没被引用的 import；from-import 部分用到时只保留用到的名字。"""
    tree = ast.parse(src)
    used = _used_names(tree)
    lines = src.splitlines(keepends=True)
    edits: list[tuple[int, int, str | None]] = []       # (start, end, replacement_line or None=删除)
    for node in tree.body:
        if isinstance(node, ast.Import):
            keep = [a for a in node.names if (a.asname or a.name.split(".")[0]) in used]
            if len(keep) == len(node.names):
                continue
            rep = None if not keep else "import " + ", ".join(a.name + (f" as {a.asname}" if a.asname else "") for a in keep) + "\n"
            edits.append((node.lineno, node.end_lineno, rep))
        elif isinstance(node, ast.ImportFrom):
            if node.module == "__future__" or any(a.name == "*" for a in node.names):
                continue
            keep = [a for a in node.names if (a.asname or a.name) in used]
            if len(keep) == len(node.names):
                continue
            mod = "." * node.level + (node.module or "")
            rep = None if not keep else f"from {mod} import " + ", ".join(a.name + (f" as {a.asname}" if a.asname else "") for a in keep) + "\n"
            edits.append((node.lineno, node.end_lineno, rep))
    for start, end, rep in sorted(edits, reverse=True):
        lines[start - 1:end] = [rep] if rep else []
    return "".join(lines)


def link_header(folder: Path) -> str:
    meta = folder / "metadata.json"
    if not meta.exists():
        return ""
    try:
        links = (json.load(open(meta, encoding="utf-8")).get("link") or {})
    except (OSError, ValueError):
        return ""
    urls = [links.get(k) for k in ("leetcode", "neetcode") if links.get(k)]
    return "".join(f"# {u}\n" for u in urls)


def make_retry(src: str, folder: Path | None = None) -> str:
    body = strip_unused_imports(stub_methods(src)).lstrip("\n")
    head = link_header(folder) if folder else ""
    return head + ("\n" if head and body else "") + body


def write_retry(folder_or_file: Path) -> Path:
    src_path = folder_or_file / "solution.py" if folder_or_file.is_dir() else folder_or_file
    dst = src_path.with_name(RETRY_NAME)
    dst.write_text(make_retry(src_path.read_text(encoding="utf-8"), src_path.parent), encoding="utf-8")
    return dst


def main(argv: list[str]) -> None:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip()); return
    if argv[0] == "--stdout":
        f = Path(argv[1])
        print(make_retry(f.read_text(encoding="utf-8"), f.parent), end="")
        return
    for a in argv:
        print(f"✅ {write_retry(Path(a))}")


if __name__ == "__main__":
    main(sys.argv[1:])
