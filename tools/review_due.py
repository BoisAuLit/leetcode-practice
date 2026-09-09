#!/usr/bin/env python3
"""
review_due.py — 间隔复习调度器（只依赖标准库）

数据源：每个题目文件夹里的 metadata.json（唯一真相）。
    <大类>/<子分类>/LC-0155 - Min Stack/
        solution.py  problem.pdf  metadata.json  [assets/]

metadata.json 里和复习有关的字段：
    info.signal / info.mode      信号 → 模式（十秒识别的训练目标）
    info.guard                   守卫反例：输入 -> 期望（必须是真实踩过的坑）
    info.sticking_point          首次做题的卡点
    info.first_date              首次做题日期
    practice: [ {date, sticking_point, result: 🟢|🟡|🔴}, ... ]   每次复习追加一条

"下次复习日期" 和 "是否毕业" 不落盘，每次从 practice[] 现算：
    间隔阶梯 1 → 3 → 7 → 14 → 30 天；🟢 升一级，🟡 不变，🔴 重置为 1 天；
    处在 30 天这一级又拿到 🟢 即毕业。

用法：
    python3 tools/review_due.py today [-n 3]          今日到期清单；不足 n 题时从"未排期"里跨分类补足
    python3 tools/review_due.py shuffle [-n 3]        同 today，并把选中的题以软链接放进 Today/（先清空）
    python3 tools/review_due.py done <子串> <g|y|r> [--note "卡点"]   记录今天的复习结果
    python3 tools/review_due.py stats                 总量、到期/排期/未排期/毕业、按大类进度、最近🔴
    python3 tools/review_due.py list [due|unscheduled|scheduled|graduated|all]
    python3 tools/review_due.py init <子串> "<信号→模式>" [--guard "..."] [--sticking "..."]
                                                      给一道题写入信号→模式（入库时通常已写好）
<子串> 匹配题目文件夹的相对路径（不区分大小写），匹配到多个时会列出候选。
"""
from __future__ import annotations
import json, os, re, sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODAY_DIR = ROOT / "Today"
INTERVALS = [1, 3, 7, 14, 30]
STATUS_MAP = {"g": "🟢", "y": "🟡", "r": "🔴", "🟢": "🟢", "🟡": "🟡", "🔴": "🔴"}
EXCLUDE_PARTS = {"__pycache__", "tools", ".git", ".vscode", "New", "Today"}
PROBLEM_DIR_RE = re.compile(r"^(LC-\d{4}|NC) - ")


# ---------------------------------------------------------------- model
@dataclass
class Problem:
    path: Path
    meta: dict

    @property
    def rel(self) -> str:
        return str(self.path.relative_to(ROOT))

    @property
    def category(self) -> str:
        return self.path.relative_to(ROOT).parts[0]

    @property
    def id(self) -> str:
        return self.meta.get("id", self.path.name)

    @property
    def title(self) -> str:
        return self.meta.get("title") or self.path.name

    @property
    def practice(self) -> list[dict]:
        return self.meta.setdefault("practice", [])

    @property
    def history(self) -> list[tuple[date, str]]:
        out = []
        for p in self.practice:
            try:
                out.append((date.fromisoformat(p["date"]), p["result"]))
            except (KeyError, ValueError):
                continue
        return sorted(out)

    def level(self) -> tuple[int, bool]:
        """根据历史推算当前间隔等级，以及是否已达毕业条件。"""
        level, graduated = 0, False
        for _, st in self.history:
            if st == "🟢":
                if level == len(INTERVALS) - 1:
                    graduated = True
                level = min(level + 1, len(INTERVALS) - 1)
            elif st == "🔴":
                level = 0
        return level, graduated

    @property
    def graduated(self) -> bool:
        return self.level()[1]

    @property
    def next_date(self) -> date | None:
        h = self.history
        if not h or self.graduated:
            return None
        last = h[-1][0]
        lvl, _ = self.level()
        from datetime import timedelta
        return last + timedelta(days=INTERVALS[lvl])

    @property
    def unscheduled(self) -> bool:
        return not self.history

    def is_due(self, today: date) -> bool:
        nd = self.next_date
        return nd is not None and nd <= today

    @property
    def first_date(self) -> date | None:
        fd = (self.meta.get("info") or {}).get("first_date")
        try:
            return date.fromisoformat(fd) if fd else None
        except ValueError:
            return None

    @property
    def signal_line(self) -> str:
        info = self.meta.get("info") or {}
        sig, mode = info.get("signal"), info.get("mode")
        if sig and mode:
            return f"{sig} → {mode}"
        return sig or mode or "（信号→模式 待补）"

    def save(self) -> None:
        with open(self.path / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)
            f.write("\n")


def load_all() -> list[Problem]:
    out = []
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in EXCLUDE_PARTS and not d.startswith("$$") and not d.startswith(".")]
        if "metadata.json" in fns and PROBLEM_DIR_RE.match(os.path.basename(dp)):
            try:
                meta = json.load(open(os.path.join(dp, "metadata.json"), encoding="utf-8"))
            except Exception as e:
                print(f"⚠️  跳过损坏的 metadata: {os.path.relpath(dp, ROOT)} ({e})", file=sys.stderr)
                continue
            out.append(Problem(Path(dp), meta))
    return sorted(out, key=lambda p: p.rel)


def resolve(target: str, problems: list[Problem]) -> Problem:
    p = Path(target)
    if p.exists():
        rp = p.resolve()
        hits = [x for x in problems if x.path == rp or rp.is_relative_to(x.path)]
        if len(hits) == 1:
            return hits[0]
    needle = target.lower()
    hits = [x for x in problems if needle in x.rel.lower()]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        sys.exit(f"找不到题目：{target}")
    sys.exit("匹配到多个题目，请给更长的子串：\n  " + "\n  ".join(x.rel for x in hits[:20]))


# ---------------------------------------------------------------- selection
def pick_today(problems: list[Problem], n: int, today: date) -> tuple[list[Problem], list[Problem]]:
    """返回 (到期题按逾期天数降序, 从未排期里补足的题)。
    补足规则 = 交错练习：按大类轮转，每个大类内部先取首次日期最早的（放得最久的）。"""
    due = [p for p in problems if p.is_due(today)]
    due.sort(key=lambda p: (p.next_date, p.rel))
    fill: list[Problem] = []
    if len(due) < n:
        pool = [p for p in problems if p.unscheduled]
        by_cat: dict[str, list[Problem]] = {}
        for p in pool:
            by_cat.setdefault(p.category, []).append(p)
        for cat in by_cat:
            by_cat[cat].sort(key=lambda p: (p.first_date or date.max, p.rel))
        # 从"已排期/毕业最少"的大类开始轮转，让冷门大类也能被叫到
        progress = {c: sum(1 for p in problems if p.category == c and not p.unscheduled) for c in by_cat}
        order = sorted(by_cat, key=lambda c: (progress[c], c))
        i = 0
        while len(due) + len(fill) < n and any(by_cat.values()):
            cat = order[i % len(order)]
            if by_cat[cat]:
                fill.append(by_cat[cat].pop(0))
            i += 1
    return due, fill


def print_selection(due: list[Problem], fill: list[Problem], today: date, n: int) -> None:
    print(f"📅 {today.isoformat()}  到期复习 {len(due)} 题" + (f"，从未排期补足 {len(fill)} 题" if fill else ""))
    k = 0
    for p in due:
        k += 1
        over = (today - p.next_date).days
        tag = f"逾期 {over} 天" if over > 0 else "今天到期"
        print(f"  {k:2d}. [{tag}] {p.id}  {p.title}   ({p.category})")
        print(f"      信号→模式: {p.signal_line}")
    for p in fill:
        k += 1
        print(f"  {k:2d}. [首次进入循环] {p.id}  {p.title}   ({p.category})")
        print(f"      信号→模式: {p.signal_line}")
    if not due and not fill:
        print("  （没有到期的题，也没有未排期的题）")


# ---------------------------------------------------------------- commands
def cmd_today(n: int) -> None:
    problems = load_all()
    today = date.today()
    due, fill = pick_today(problems, n, today)
    print_selection(due, fill, today, n)
    left = sum(1 for p in problems if p.unscheduled) - len(fill)
    print(f"\n未排期剩余 {left} 题 ｜ 完成一题后执行: python3 tools/review_due.py done <子串> <g|y|r> [--note \"卡点\"]")
    print("把今天的题放进 Today/ 文件夹: python3 tools/review_due.py shuffle" + (f" -n {n}" if n != 3 else ""))


def cmd_shuffle(n: int) -> None:
    problems = load_all()
    today = date.today()
    due, fill = pick_today(problems, n, today)
    TODAY_DIR.mkdir(exist_ok=True)
    kept = []
    for entry in sorted(TODAY_DIR.iterdir()):
        if entry.is_symlink():
            entry.unlink()
        elif entry.name != ".DS_Store":
            kept.append(entry.name)          # 只清软链接，绝不删真实文件
    if kept:
        print(f"⚠️  Today/ 里有非软链接的文件，未动: {kept}")
    chosen = due + fill
    for i, p in enumerate(chosen, start=1):
        link = TODAY_DIR / f"{i:02d} - {p.path.name}"
        link.symlink_to(os.path.relpath(p.path, TODAY_DIR), target_is_directory=True)
    print_selection(due, fill, today, n)
    print(f"\n✅ Today/ 已更新：{len(chosen)} 个软链接 → 各题的文件夹")


def cmd_done(target: str, status: str, note: str | None) -> None:
    st = STATUS_MAP.get(status.lower() if status.isascii() else status)
    if not st:
        sys.exit("状态只能是 g / y / r（或 🟢 🟡 🔴）")
    problems = load_all()
    p = resolve(target, problems)
    if p.graduated:
        sys.exit(f"这题已经毕业了：{p.rel}")
    p.practice.append({"date": date.today().isoformat(), "sticking_point": note or "", "result": st})
    p.save()
    lvl, grad = p.level()
    if grad:
        print(f"{st} 已记录 → {p.rel}\n   🎓 毕业！不再叫号（档案永远留在 metadata.json 里）")
    else:
        print(f"{st} 已记录 → {p.rel}\n   下次复习: {p.next_date.isoformat()}（{INTERVALS[lvl]} 天后）")


def cmd_stats() -> None:
    problems = load_all()
    today = date.today()
    due = [p for p in problems if p.is_due(today)]
    sched = [p for p in problems if p.next_date and not p.is_due(today)]
    unsch = [p for p in problems if p.unscheduled]
    grad = [p for p in problems if p.graduated]
    print(f"题目总数 {len(problems)} ｜ 到期 {len(due)} ｜ 已排期未到 {len(sched)} ｜ 未排期 {len(unsch)} ｜ 毕业 {len(grad)}")
    print("\n按大类：      总数  到期  排期  未排期  毕业")
    cats = sorted({p.category for p in problems})
    for c in cats:
        ps = [p for p in problems if p.category == c]
        d = sum(1 for p in ps if p.is_due(today)); s = sum(1 for p in ps if p.next_date and not p.is_due(today))
        u = sum(1 for p in ps if p.unscheduled); g = sum(1 for p in ps if p.graduated)
        print(f"  {c[:34]:34s} {len(ps):4d}  {d:4d}  {s:4d}  {u:6d}  {g:4d}")
    reds = sorted(((h[0], p) for p in problems for h in p.history if h[1] == "🔴"), key=lambda x: x[0], reverse=True)[:8]
    if reds:
        print("\n最近的 🔴：")
        for d, p in reds:
            print(f"  {d}  {p.id}  {p.title}")
    done_today = sum(1 for p in problems for h in p.history if h[0] == today)
    print(f"\n今日已完成复习 {done_today} 题")


def cmd_list(which: str) -> None:
    problems = load_all()
    today = date.today()
    sel = {
        "due": lambda p: p.is_due(today),
        "unscheduled": lambda p: p.unscheduled,
        "scheduled": lambda p: p.next_date is not None and not p.is_due(today),
        "graduated": lambda p: p.graduated,
        "all": lambda p: True,
    }.get(which)
    if not sel:
        sys.exit("list 后面只能是 due | unscheduled | scheduled | graduated | all")
    rows = [p for p in problems if sel(p)]
    for p in rows:
        if p.graduated:
            state = "毕业 ✅"
        elif p.next_date:
            state = f"下次 {p.next_date.isoformat()}"
        else:
            state = "未排期"
        hist = " ".join(h[1] for h in p.history) or "-"
        print(f"{state:14s} {hist:8s} {p.rel}")
    print(f"\n共 {len(rows)} 题")


def cmd_init(target: str, signal: str, guard: str | None, sticking: str | None) -> None:
    problems = load_all()
    p = resolve(target, problems)
    info = p.meta.setdefault("info", {})
    if "→" in signal:
        a, b = signal.split("→", 1)
        info["signal"], info["mode"] = a.strip(), b.strip()
    else:
        info["signal"] = signal.strip()
    if guard is not None:
        info["guard"] = guard
    if sticking is not None:
        info["sticking_point"] = sticking
    info.setdefault("first_date", date.today().isoformat())
    p.save()
    print(f"✅ 已写入 {p.rel}/metadata.json\n   信号→模式: {p.signal_line}")


# ---------------------------------------------------------------- main
def _flag(argv: list[str], name: str) -> str | None:
    if name in argv:
        i = argv.index(name)
        if i + 1 < len(argv):
            v = argv[i + 1]
            del argv[i:i + 2]
            return v
        sys.exit(f"{name} 后面需要一个值")
    return None


def main(argv: list[str]) -> None:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip()); return
    cmd, rest = argv[0], argv[1:]
    n = int(_flag(rest, "-n") or 3)
    if cmd == "today":
        cmd_today(n)
    elif cmd == "shuffle":
        cmd_shuffle(n)
    elif cmd == "done":
        note = _flag(rest, "--note")
        if len(rest) != 2:
            sys.exit('用法: done <子串> <g|y|r> [--note "卡点"]')
        cmd_done(rest[0], rest[1], note)
    elif cmd == "stats":
        cmd_stats()
    elif cmd == "list":
        cmd_list(rest[0] if rest else "due")
    elif cmd == "init":
        guard, sticking = _flag(rest, "--guard"), _flag(rest, "--sticking")
        if len(rest) != 2:
            sys.exit('用法: init <子串> "<信号→模式>" [--guard "..."] [--sticking "..."]')
        cmd_init(rest[0], rest[1], guard, sticking)
    else:
        sys.exit(f"未知命令: {cmd}\n\n{__doc__.strip()}")


if __name__ == "__main__":
    main(sys.argv[1:])
