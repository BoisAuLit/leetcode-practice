#!/usr/bin/env python3
"""
review_due.py — 间隔复习调度器（只依赖标准库）

它读写的是每个解答文件顶部的"复习头"（模块 docstring）：

    \"\"\"
    📌 信号→模式: 两个序列各一个指针 → 双序列 DP（LCS 家族）
    📅 首次: 2026-09-04 | 卡点: M1 边界层右列漏 break | 守卫: ("ba","c","cbx")->False
    🔁 复习: 2026-09-05 🟡 | 2026-09-08 🟢 | 下次: 2026-09-15
    \"\"\"

复习行只有三种形态：
    🔁 复习: 未排期
    🔁 复习: <历史...> | 下次: YYYY-MM-DD
    🔁 复习: <历史...> | 毕业 ✅

用法（在仓库任意位置执行）：
    python3 tools/review_due.py today [-n 3]
        列出今日到期的复习；不足 n 题时，从"未排期"里跨分类轮转补足，并把补进来的标为今日到期。
    python3 tools/review_due.py done <文件路径或唯一子串> <g|y|r>
        记录今天的复习结果：g=🟢 闭卷流畅  y=🟡 有印象但慢  r=🔴 卡壳/想不出
    python3 tools/review_due.py stats
    python3 tools/review_due.py list [due|unscheduled|scheduled|graduated|all]
    python3 tools/review_due.py init <文件路径> "<信号→模式一句话>"
        给一个还没有复习头的新文件加头（首次=今天，卡点/守卫留待补，未排期）。

节奏：🟢 → 间隔升级 1→3→7→14→30 天；🟡 → 间隔不变；🔴 → 重置为 1 天；
      在 30 天间隔之后再得一个 🟢 → 毕业（连续 5 个 🟢）。
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INTERVALS = [1, 3, 7, 14, 30]
HEADER_SCAN_LINES = 15
EXCLUDE_PARTS = {"__pycache__", "tools", ".git", ".vscode"}

SIG_RE = re.compile(r"📌\s*信号→模式:\s*(.*)")
FIRST_RE = re.compile(r"📅\s*首次:\s*(\S*)\s*\|\s*卡点:\s*(.*?)\s*\|\s*守卫:\s*(.*)")
REVIEW_RE = re.compile(r"🔁\s*复习:\s*(.*)")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STATUS_MAP = {"g": "🟢", "y": "🟡", "r": "🔴", "🟢": "🟢", "🟡": "🟡", "🔴": "🔴"}


@dataclass
class Header:
    path: Path
    signal: str = ""
    first: str = ""
    blocker: str = ""
    guard: str = ""
    history: list[tuple[str, str]] = field(default_factory=list)  # [(date, status)]
    next_date: date | None = None
    graduated: bool = False
    review_line_no: int = -1

    @property
    def rel(self) -> str:
        return str(self.path.relative_to(ROOT))

    @property
    def category(self) -> str:
        return self.path.relative_to(ROOT).parts[0]

    @property
    def unscheduled(self) -> bool:
        return self.next_date is None and not self.graduated

    def is_due(self, today: date) -> bool:
        return self.next_date is not None and self.next_date <= today and not self.graduated

    def level(self) -> tuple[int, bool]:
        """根据历史推算下一次间隔等级，以及是否已达毕业条件。"""
        level, graduated = 0, False
        for _, st in self.history:
            if st == "🟢":
                if level == len(INTERVALS) - 1:
                    graduated = True
                level = min(level + 1, len(INTERVALS) - 1)
            elif st == "🔴":
                level = 0
        return level, graduated

    def review_line(self) -> str:
        parts = [f"{d} {s}" for d, s in self.history]
        if self.graduated:
            parts.append("毕业 ✅")
        elif self.next_date is not None:
            parts.append(f"下次: {self.next_date.isoformat()}")
        else:
            return "🔁 复习: 未排期"
        return "🔁 复习: " + " | ".join(parts)


def iter_py_files() -> list[Path]:
    out = []
    for p in ROOT.rglob("*.py"):
        parts = p.relative_to(ROOT).parts
        if any(part in EXCLUDE_PARTS or part.startswith("$$") for part in parts):
            continue
        out.append(p)
    return sorted(out)


def parse_header(path: Path) -> Header | None:
    try:
        with open(path, encoding="utf-8") as f:
            head = [next(f) for _ in range(HEADER_SCAN_LINES)]
    except StopIteration:
        with open(path, encoding="utf-8") as f:
            head = f.readlines()
    except (UnicodeDecodeError, OSError):
        return None

    h = Header(path=path)
    found = False
    for i, line in enumerate(head):
        if m := SIG_RE.search(line):
            h.signal, found = m.group(1).strip(), True
        elif m := FIRST_RE.search(line):
            h.first, h.blocker, h.guard = m.group(1), m.group(2).strip(), m.group(3).strip()
        elif m := REVIEW_RE.search(line):
            h.review_line_no = i
            for tok in (t.strip() for t in m.group(1).split("|")):
                if not tok or tok == "未排期":
                    continue
                if tok.startswith("下次:"):
                    h.next_date = date.fromisoformat(tok.split(":", 1)[1].strip())
                elif tok.startswith("毕业"):
                    h.graduated = True
                else:
                    d, _, st = tok.partition(" ")
                    if DATE_RE.match(d) and st.strip() in STATUS_MAP:
                        h.history.append((d, STATUS_MAP[st.strip()]))
    return h if found and h.review_line_no >= 0 else None


def load_all() -> list[Header]:
    return [h for p in iter_py_files() if (h := parse_header(p))]


def write_review_line(h: Header) -> None:
    with open(h.path, encoding="utf-8") as f:
        lines = f.read().splitlines(keepends=True)
    old = lines[h.review_line_no]
    eol = "\n" if old.endswith("\n") else ""
    lines[h.review_line_no] = h.review_line() + eol
    with open(h.path, "w", encoding="utf-8") as f:
        f.write("".join(lines))


def resolve(target: str, headers: list[Header]) -> Header:
    p = Path(target)
    cands = [h for h in headers if h.path == p.resolve()] if p.exists() else []
    if not cands:
        needle = target.lower()
        cands = [h for h in headers if needle in h.rel.lower()]
    if len(cands) == 1:
        return cands[0]
    if not cands:
        sys.exit(f"找不到带复习头的文件：{target}")
    sys.exit("匹配到多个文件，请更精确：\n  " + "\n  ".join(h.rel for h in cands))


# ---------------------------------------------------------------- commands
def cmd_today(n: int) -> None:
    today = date.today()
    headers = load_all()
    due = sorted((h for h in headers if h.is_due(today)), key=lambda h: (h.next_date, h.rel))

    print(f"📅 {today.isoformat()}  到期复习 {len(due)} 题")
    for h in due:
        overdue = (today - h.next_date).days
        tag = f"（逾期 {overdue} 天）" if overdue > 0 else ""
        print(f"  • {h.rel}{tag}\n      {h.signal}")

    need = n - len(due)
    if need > 0:
        pool = [h for h in headers if h.unscheduled]
        by_cat: dict[str, list[Header]] = {}
        for h in sorted(pool, key=lambda h: (h.first or "9999", h.rel)):
            by_cat.setdefault(h.category, []).append(h)
        picked: list[Header] = []
        cats = sorted(by_cat)
        while len(picked) < need and any(by_cat.values()):
            for c in cats:  # 跨分类轮转 = 交错练习
                if by_cat[c] and len(picked) < need:
                    picked.append(by_cat[c].pop(0))
        if picked:
            print(f"\n🆕 新纳入 {len(picked)} 题（未排期 → 今日到期）")
            for h in picked:
                h.next_date = today
                write_review_line(h)
                print(f"  • {h.rel}\n      {h.signal}")
    left = sum(1 for h in headers if h.unscheduled)  # 刚纳入的已带 next_date，自动不再计入
    print(f"\n未排期剩余 {left} 题 ｜ 完成一题后执行: python3 tools/review_due.py done <子串> <g|y|r>")


def cmd_done(target: str, status: str) -> None:
    st = STATUS_MAP.get(status)
    if not st:
        sys.exit("状态请用 g / y / r（或 🟢 🟡 🔴）")
    headers = load_all()
    h = resolve(target, headers)
    if h.graduated:
        sys.exit(f"{h.rel} 已毕业，无需再记。")
    today = date.today()
    h.history.append((today.isoformat(), st))
    level, graduated = h.level()
    if graduated:
        h.graduated, h.next_date = True, None
        write_review_line(h)
        print(f"🎓 毕业！{h.rel}")
        return
    h.next_date = today + timedelta(days=INTERVALS[level])
    write_review_line(h)
    print(f"{st} 已记录 → {h.rel}\n   下次复习: {h.next_date.isoformat()}（{INTERVALS[level]} 天后）")


def cmd_stats() -> None:
    today = date.today()
    all_py = iter_py_files()
    headers = load_all()
    due = [h for h in headers if h.is_due(today)]
    uns = [h for h in headers if h.unscheduled]
    grad = [h for h in headers if h.graduated]
    sched = [h for h in headers if h.next_date is not None and not h.is_due(today)]
    print(f"文件总数 {len(all_py)} ｜ 有复习头 {len(headers)} ｜ 无头 {len(all_py) - len(headers)}")
    print(f"到期 {len(due)} ｜ 已排期未到 {len(sched)} ｜ 未排期 {len(uns)} ｜ 已毕业 {len(grad)}")
    print("\n按分类：")
    cats: dict[str, dict[str, int]] = {}
    for h in headers:
        c = cats.setdefault(h.category, {"总": 0, "到期": 0, "未排期": 0, "毕业": 0, "🔴": 0})
        c["总"] += 1
        c["到期"] += h.is_due(today)
        c["未排期"] += h.unscheduled
        c["毕业"] += h.graduated
        c["🔴"] += bool(h.history) and h.history[-1][1] == "🔴"
    for cat in sorted(cats):
        c = cats[cat]
        print(f"  {cat}: 总 {c['总']} ｜ 到期 {c['到期']} ｜ 未排期 {c['未排期']} ｜ 毕业 {c['毕业']} ｜ 最近🔴 {c['🔴']}")
    done_today = sum(1 for h in headers for d, _ in h.history if d == today.isoformat())
    print(f"\n今日已完成复习 {done_today} 题")


def cmd_list(which: str) -> None:
    today = date.today()
    headers = load_all()
    sel = {
        "due": [h for h in headers if h.is_due(today)],
        "unscheduled": [h for h in headers if h.unscheduled],
        "scheduled": sorted((h for h in headers if h.next_date and not h.is_due(today)), key=lambda h: h.next_date),
        "graduated": [h for h in headers if h.graduated],
        "all": headers,
    }.get(which)
    if sel is None:
        sys.exit("list 参数: due | unscheduled | scheduled | graduated | all")
    for h in sel:
        nxt = "毕业" if h.graduated else (h.next_date.isoformat() if h.next_date else "未排期")
        print(f"{nxt}  {h.rel}")
    print(f"共 {len(sel)} 题")


def cmd_init(target: str, signal: str) -> None:
    p = Path(target).resolve()
    if not p.exists():
        sys.exit(f"文件不存在：{target}")
    if parse_header(p):
        sys.exit("该文件已有复习头。")
    header = (
        '"""\n'
        f"📌 信号→模式: {signal}\n"
        f"📅 首次: {date.today().isoformat()} | 卡点: （待补） | 守卫: （待补）\n"
        "🔁 复习: 未排期\n"
        '"""\n'
    )
    content = p.read_text(encoding="utf-8")
    p.write_text(header + content, encoding="utf-8")
    print(f"已加头：{p.relative_to(ROOT)}")


def main(argv: list[str]) -> None:
    if not argv or argv[0] in {"-h", "--help", "help"}:
        print(__doc__)
        return
    cmd, args = argv[0], argv[1:]
    if cmd == "today":
        n = 3
        if len(args) >= 2 and args[0] == "-n":
            n = int(args[1])
        cmd_today(n)
    elif cmd == "done":
        if len(args) != 2:
            sys.exit("用法: done <文件路径或唯一子串> <g|y|r>")
        cmd_done(args[0], args[1])
    elif cmd == "stats":
        cmd_stats()
    elif cmd == "list":
        cmd_list(args[0] if args else "due")
    elif cmd == "init":
        if len(args) != 2:
            sys.exit('用法: init <文件路径> "<信号→模式>"')
        cmd_init(args[0], args[1])
    else:
        sys.exit(f"未知命令 {cmd}；执行 --help 查看用法")


if __name__ == "__main__":
    main(sys.argv[1:])
