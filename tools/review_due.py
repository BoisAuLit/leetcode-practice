#!/usr/bin/env python3
"""
review_due.py — 间隔复习调度器（只依赖标准库）

数据源：每个题目文件夹里的 metadata.json（唯一真相）。
    <大类>/<子分类>/LC-0155 - Min Stack/
        solution.py  problem.pdf  problem_dark.pdf  metadata.json  [note.md]  [asset-*]

metadata.json 里和复习有关的字段：
    path                         该题相对仓库根目录的路径（题目文件夹被挪动后 load_all 会自动修正）
    practice: [ {date, sticking_point, result: 🟢|🟡|🔴}, ... ]   每次复习追加一条
题目标题、信号→模式都不进 metadata：全在文件夹名里（LC-0155 - Min Stack - <信号/备注>），复习时看文件夹名就够了。

"下次复习日期" 和 "是否毕业" 不落盘，每次从 practice[] 现算：
    间隔阶梯 1 → 3 → 7 → 14 → 30 → 60 天；🟢 升一级，🟡 不变，🔴 重置为 1 天；
    逾期很久才做、却拿到 🟢 的题，直接跳到第一个比实际间隔更长的档位（记忆既然撑过了 45 天，就不必再回头走 14 天）；
    处在 60 天这一级又拿到 🟢 即毕业。

叫号规则（shuffle / today）：到期题优先。全部到期题先按上次颜色排（🔴 > 🟡 > 🟢），同色再按逾期天数（越久越前），同分随机，取前 k 题
    （k = -n，shuffle / today 默认 7）；到期题不够 k 道才用从未复习过的题补足：核心层（tools/nc150.txt）优先，按大类轮转交错；
    没到期的题绝不出现（避免同一批题天天见）；抽完再随机打乱一次顺序，Today/ 里的编号不可预测。

用法：
    python3 tools/review_due.py today [-n 7]          今日清单（只打印，不动 Today/）
    python3 tools/review_due.py shuffle [-n 7] [--reset]
                                                      同 today，并把选中的题以软链接放进 Today/（先清空），
                                                      每题文件夹里生成闭卷重写用的 solution_retry.py；
                                                      --reset 才会顺便把 LeetCode / NeetCode 网站上的旧代码重置（默认不去网站）
    python3 tools/review_due.py reset [序号]          对 Today/ 里的题（或某一题）做网站代码重置（LeetCode / NeetCode）
    python3 tools/review_due.py finish <序号|题目文件夹路径> [g|y|r]
                                                      数字 = Today/ 里的序号；路径 = 任意题目文件夹（必须存在且有 solution_retry.py，否则报错）。
                                                      记结果（默认 g），Today/ 里有它的软链接就移除；
                                                      如果这是 Today/ 里最后一题，自动再 shuffle AUTO_SHUFFLE_N 题；
                                                      solution_retry.py 里带 # 注释的 class 先存进该题 note.md（### 📝 日期 - retry N），再删文件
    python3 tools/review_due.py remove <序号|题目文件夹路径> [--dry-run]
                                                      把一道题彻底从题库里剔除（给"这题对我没用"的情况）。
                                                      数字 = Today/ 里的序号；路径 = 任意题目文件夹。
                                                      题目文件夹整个移进 macOS 废纸篓（可恢复，不用 rm：PDF/图片被 gitignore，git 救不回来）；
                                                      顺带清掉 Today/ 软链接、空掉的子分类文件夹、各 README 里引用它的表格行，最后刷新 progress.md。
                                                      --dry-run 只看会动什么，不真删。
    python3 tools/review_due.py done <子串> <g|y|r> [--note "卡点"]   按题目名记录今天的复习结果
    python3 tools/review_due.py stats                 总量、到期/排期/未排期/毕业、按大类进度、最近🔴
    python3 tools/review_due.py mono [--apply]        列出疑似单调栈/单调队列、却不在 18 专区的题（关键词命中：文件夹名 / solution.py / metadata.json / note.md）；
                                                      只是提醒，--apply 才真的搬进 18-monotonic/general（shuffle 本身不再搬任何文件）
    python3 tools/review_due.py list [due|unscheduled|scheduled|graduated|all|core]
<子串> 匹配题目文件夹的相对路径（不区分大小写），匹配到多个时会列出候选。
"""
from __future__ import annotations
import json, os, random, re, shutil, subprocess, sys, urllib.parse
from dataclasses import dataclass, field
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_retry import write_retry, RETRY_NAME  # noqa: E402

NOTE_NAME = "note.md"        # 每题的笔记，和 solution.py 同级；solution_retry.py 里带注释的 class（finish 时）和 done --note 的卡点进这里

ROOT = Path(__file__).resolve().parent.parent
TODAY_DIR = ROOT / "Today"
INTERVALS = [1, 3, 7, 14, 30, 60]
STATUS_MAP = {"g": "🟢", "y": "🟡", "r": "🔴", "🟢": "🟢", "🟡": "🟡", "🔴": "🔴"}
EXCLUDE_PARTS = {"__pycache__", "tools", ".git", ".vscode", "New", "Today"}
PROBLEM_DIR_RE = re.compile(r"^(?:\d{1,2} *- *)?(LC-\d{4}|NC) - ")   # 可选的数字优先级前缀，两种写法都认：01-LC-0876 - Title / 01 - LC-0743 - Title
ETSY = Path("/Users/bohaoli/Desktop/tuto/tuto_etsy")                 # puppeteer 脚本所在项目（和抓 PDF 共用）
RESET_SCRIPT = "VV-utils/11-reset-code.ts"                           # 清空 LeetCode / NeetCode 在线编辑器里的旧代码
CANARY_URL = "http://127.0.0.1:9222/json/version"
# 所有和单调栈 / 单调队列沾边的题一律归到这个大类（intake 强制执行；shuffle 只提醒，`mono --apply` 才搬）
MONO_CAT = "18-monotonic-fuck-you (单调栈、单调队列)"
MONO_RE = re.compile(r"monotonic|单调(栈|队列|递增栈|递减栈|双端)", re.I)
CORE_FILE = ROOT / "tools" / "nc150.txt"   # 核心层（NeetCode 150）：每行一个 LC-xxxx，# 后面是注释


def load_core() -> set[str]:
    """读 tools/nc150.txt 里的题号集合；文件不存在就返回空集（所有题平等）。"""
    if not CORE_FILE.exists():
        return set()
    out = set()
    for line in CORE_FILE.read_text(encoding="utf-8").splitlines():
        tok = line.split("#", 1)[0].strip()
        if tok:
            out.add(tok)
    return out


CORE_IDS = load_core()


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
        """文件夹名去掉 'LC-0155 - ' / 'NC - ' 前缀；挂在标题后面的信号/备注一起带着。"""
        return PROBLEM_DIR_RE.sub("", self.path.name, count=1)

    @property
    def core(self) -> bool:
        """是否属于核心层（NeetCode 150）：shuffle 先清它们，stats 单独统计。"""
        return self.id in CORE_IDS

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
        """根据历史推算当前间隔等级，以及是否已达毕业条件。
        🟢：升一级；如果这次距上次复习已经隔了很久（逾期才做），直接跳到第一个比实际间隔更长的档位 ——
            记忆既然撑过了那么多天，低档位已经被证明，不必再走一遍（SM-2 的思路）。
        🟡：原地不动。🔴：重置到第 0 档（1 天）。处在最高档又拿到 🟢 即毕业。"""
        level, graduated = 0, False
        prev: date | None = None
        top = len(INTERVALS) - 1
        for d, st in self.history:
            if st == "🟢":
                if level == top:
                    graduated = True
                elapsed = (d - prev).days if prev else 0
                proven = next((i for i, iv in enumerate(INTERVALS) if iv > elapsed), top)
                level = min(max(level + 1, proven), top)
            elif st == "🔴":
                level = 0
            prev = d
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
        return last + timedelta(days=INTERVALS[lvl])

    @property
    def unscheduled(self) -> bool:
        return not self.history

    def is_due(self, today: date) -> bool:
        nd = self.next_date
        return nd is not None and nd <= today

    def save(self) -> None:
        self.meta["path"] = self.rel          # key 已存在时原地更新，不会跑到末尾去
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
            prob = Problem(Path(dp), meta)
            if meta.get("path") != prob.rel:   # 文件夹被挪过（手动移动 / 单调题强制归类）→ 自动修正
                repair_path(prob)
            out.append(prob)
    return sorted(out, key=lambda p: p.rel)


def repair_path(p: Problem) -> None:
    """把 metadata.json 里的 path 改成当前真实位置，位置保持在 id 之后。"""
    old, new = p.meta.get("path"), p.rel
    fixed = {}
    for k, v in p.meta.items():
        if k == "path":
            continue
        fixed[k] = v
        if k == "id":
            fixed["path"] = new
    if "path" not in fixed:
        fixed = {"path": new, **fixed}
    p.meta.clear(); p.meta.update(fixed)
    with open(p.path / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(p.meta, f, ensure_ascii=False, indent=2); f.write("\n")
    print(f"🔧 path 已修正：{old!r} → {new!r}", file=sys.stderr)


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
COLOUR_RANK = {"🔴": 2, "🟡": 1, "🟢": 0}   # 到期题排序：先看上次颜色（卡壳的最先），同色再看逾期天数


def priority(p: Problem, today: date) -> tuple[int, int]:
    """到期题的优先级：(上次颜色等级, 逾期天数)，越大越先。同分随机（调用方先 shuffle 再 sort）。"""
    over = (today - p.next_date).days if p.next_date else 0
    last = p.history[-1][1] if p.history else ""
    return (COLOUR_RANK.get(last, 0), over)


SHUFFLE_N = 7                      # shuffle / today 不带 -n 时的默认题数
LEECH_REDS = 3                     # 累计 🔴 达到这个数就标 🩸 顽固题：别再硬刷，去读解法 / 拆成更小的模板
AUTO_SHUFFLE_N = SHUFFLE_N         # finish / remove 掉 Today/ 里最后一题之后，自动再 shuffle 这么多题


def pick_new(problems: list[Problem], k: int) -> list[Problem]:
    """从未复习过的题里按大类轮转随机抽 k 题（从进入循环最少的大类开始，交错练习）。
    核心层（tools/nc150.txt）优先：只要还有核心题没进入循环，新题就只从核心题里抽；核心层清空后才轮到其他题。"""
    pool = [p for p in problems if p.unscheduled]
    core_pool = [p for p in pool if p.core]
    if core_pool:
        pool = core_pool
    by_cat: dict[str, list[Problem]] = {}
    for p in pool:
        by_cat.setdefault(p.category, []).append(p)
    for cat in by_cat:
        random.shuffle(by_cat[cat])
    progress = {c: sum(1 for p in problems if p.category == c and not p.unscheduled) for c in by_cat}
    order = list(by_cat); random.shuffle(order); order.sort(key=lambda c: progress[c])
    out: list[Problem] = []
    i = 0
    while len(out) < k and any(by_cat.values()):
        cat = order[i % len(order)]
        if by_cat[cat]:
            out.append(by_cat[cat].pop())
        i += 1
    return out


def pick_today(problems: list[Problem], n: int, today: date) -> tuple[list[Problem], list[Problem]]:
    """到期题优先：全部到期题按 priority 排序（同分随机）取前 n 题；不够 n 道才用从未复习过的题补足。
    没到期的题绝不出现 —— 刚拿 🟢 的题要等它的日期到了才会再见。返回 (抽中的到期题, 抽中的新题)。"""
    due = [p for p in problems if p.is_due(today)]
    random.shuffle(due)
    due.sort(key=lambda p: priority(p, today), reverse=True)
    chosen_due = due[:n]
    fill = pick_new(problems, n - len(chosen_due)) if len(chosen_due) < n else []
    return chosen_due, fill


def tag_of(p: Problem, today: date) -> str:
    star = "★ " if p.core else ""
    if p.unscheduled:
        return star + "首次进入循环"
    over = (today - p.next_date).days
    last = p.history[-1][1]
    reds = sum(1 for _, st in p.history if st == "🔴")
    leech = f" 🩸🔴×{reds}" if reds >= LEECH_REDS else ""
    t = f"逾期 {over} 天" if over > 0 else ("今天到期" if over == 0 else f"{-over} 天后到期")
    return f"{star}{t} · 上次{last}{leech}"


def print_selection(chosen: list[Problem], today: date, n_due: int, n_fill: int, total_due: int) -> None:
    print(f"📅 {today.isoformat()}  抽了 {n_due + n_fill} 题：到期 {n_due} ＋ 首次进入循环 {n_fill}"
          f"（今天到期共 {total_due} 题；到期题优先，🔴 > 🟡 > 🟢，同色按逾期天数）")
    for k, p in enumerate(chosen, start=1):
        print(f"  {k:2d}. [{tag_of(p, today)}] {p.id}  {p.title}   ({p.category})")
    if not chosen:
        print("  （没有到期的题，也没有未排期的题）")


# ---------------------------------------------------------------- commands
def cmd_today(n: int) -> None:
    problems = load_all()
    today = date.today()
    due, fill = pick_today(problems, n, today)
    print_selection(due + fill, today, len(due), len(fill), sum(1 for p in problems if p.is_due(today)))
    left = sum(1 for p in problems if p.unscheduled) - len(fill)
    print(f"\n未排期剩余 {left} 题 ｜ 把今天的题放进 Today/: shuffle {n}   做完一题: finish <序号> [g|y|r]")


def _canary_running() -> bool:
    import urllib.request
    try:
        urllib.request.urlopen(CANARY_URL, timeout=2).read(); return True
    except Exception:  # noqa: BLE001
        return False


def reset_online(problems: list[Problem]) -> None:
    """在 LeetCode / NeetCode 网站上把这些题的在线代码重置为默认模板（防剧透）。
    通过 tuto_etsy 的 puppeteer 脚本操作 9222 端口上已登录的 Chrome Canary；Canary 没开就跳过并提醒。"""
    import subprocess
    urls = []
    for p in problems:
        link = p.meta.get("link") or {}
        urls += [u for u in (link.get("leetcode"), link.get("neetcode")) if u]
    if not urls:
        return
    if not _canary_running():
        print(f"⚠️  Chrome Canary 没在 9222 端口运行，跳过网站代码重置（先 `canary`，再 `review reset`）")
        return
    print(f"🧹 正在重置 {len(urls)} 个网页上的旧代码（LeetCode / NeetCode）...", flush=True)
    ok, fail = [], []
    proc = subprocess.Popen(["npx", "tsx", RESET_SCRIPT, *urls], cwd=ETSY, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    for line in proc.stdout:
        line = line.strip()
        if line.startswith("RESET_OK "):
            ok.append(line[9:]); print(f"   ✓ {line[9:]}", flush=True)
        elif line.startswith("RESET_FAIL "):
            fail.append(line[11:]); print(f"   ✗ {line[11:]}", flush=True)
    proc.wait()
    print(f"   网站代码重置：成功 {len(ok)} / {len(urls)}" + (f"，失败 {len(fail)}（可 `review reset` 重试）" if fail else ""))


def _today_links(idx: int | None = None) -> list[Path]:
    if not TODAY_DIR.is_dir():
        return []
    links = sorted(e for e in TODAY_DIR.iterdir() if e.is_symlink())
    if idx is not None:
        links = [e for e in links if e.name.startswith(f"{idx:02d} - ")]
    return links


def cmd_reset(idx: int | None) -> None:
    """对 Today/ 里的题（或指定序号那一题）重跑网站代码重置。"""
    links = _today_links(idx)
    if not links:
        sys.exit("Today/ 里没有题" + (f"（序号 {idx}）" if idx else "") + "，先 shuffle")
    problems = load_all()
    targets = [x for l in links for x in problems if x.path == l.resolve()]
    reset_online(targets)


def mono_reason(p: Problem) -> str | None:
    """这题为什么被当成单调题：文件夹名 / solution.py / metadata.json / note.md 里第一处命中 MONO_RE 的位置。没命中返回 None。"""
    m = MONO_RE.search(p.path.name)
    if m:
        return f"文件夹名含「{m.group(0)}」"
    for f in ("solution.py", "metadata.json", NOTE_NAME):
        fp = p.path / f
        try:
            if not fp.exists():
                continue
            for ln, line in enumerate(fp.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                m = MONO_RE.search(line)
                if m:
                    return f"{f}:{ln} 含「{m.group(0)}」"
        except OSError:
            pass
    return None


def is_monotonic(p: Problem) -> bool:
    return mono_reason(p) is not None


def monotonic_strays(problems: list[Problem]) -> list[tuple[Problem, str]]:
    """不在 MONO_CAT、却命中单调关键词的题（纯文字匹配，注释里顺口提一句也算，所以只提醒不自动搬）。"""
    out = []
    for p in problems:
        if p.category == MONO_CAT:
            continue
        why = mono_reason(p)
        if why:
            out.append((p, why))
    return out


def cmd_mono(apply: bool) -> None:
    problems = load_all()
    strays = monotonic_strays(problems)
    if not strays:
        print(f"✅ 没有散落在 {MONO_CAT} 之外的单调题")
        return
    for p, why in strays:
        print(f"  {p.rel}\n     ← {why}")
    if not apply:
        print(f"\n以上 {len(strays)} 道只是关键词命中（可能误伤）。确认要搬：review mono --apply；不想再被提醒就改掉命中的那处文字。")
        return
    import shutil
    dest_dir = ROOT / MONO_CAT / "general"
    dest_dir.mkdir(parents=True, exist_ok=True)
    for p, _ in strays:
        dest = dest_dir / p.path.name
        if dest.exists():
            print(f"⚠️  {p.rel}：{dest.relative_to(ROOT)} 已存在，未动")
            continue
        shutil.move(str(p.path), str(dest))
        print(f"📦 {p.rel}  →  {dest.relative_to(ROOT)}")
    load_all()                                   # 顺手修正 metadata.json 里的 path
    print("提醒：README 里指向旧位置的链接要自己改；然后 python3 tools/progress.py")


def cmd_shuffle(n: int, reset: bool = False) -> None:
    today = date.today()
    TODAY_DIR.mkdir(exist_ok=True)
    # ① 先清场：Today/ 里每个软链接指向的题，删掉它的 solution_retry.py，再删软链接。全部清完才开始选题。
    kept, dropped = [], []
    for entry in sorted(TODAY_DIR.iterdir()):
        if entry.is_symlink():
            _remove_retry(entry)
            dropped.append(entry.name)
            entry.unlink()
        elif entry.name != ".DS_Store":
            kept.append(entry.name)          # 只清软链接，绝不删真实文件
    if kept:
        print(f"⚠️  Today/ 里有非软链接的文件，未动: {kept}")
    if dropped:
        print(f"♻️  清掉上一轮未 finish 的 {len(dropped)} 题: " + "、".join(d.split(" - ", 1)[-1] for d in dropped))
    # ② 选题：到期题优先（🔴 > 🟡 > 🟢，再按逾期），不够才补新题。散落在外的单调题只提醒，不搬（要搬：review mono --apply）
    problems = load_all()
    strays = monotonic_strays(problems)
    if strays:
        print(f"⚠️  {len(strays)} 道题疑似单调栈/单调队列却不在 {MONO_CAT}（只提醒，不搬；要搬：review mono --apply）：")
        for p, why in strays:
            print(f"     {p.rel}   ← {why}")
    due, fill = pick_today(problems, n, today)
    # ③ 打乱顺序再编号，让 Today/ 里的顺序不可预测
    chosen = due + fill
    random.shuffle(chosen)
    for i, p in enumerate(chosen, start=1):
        link = TODAY_DIR / f"{i:02d} - {p.path.name}"
        link.symlink_to(os.path.relpath(p.path, TODAY_DIR), target_is_directory=True)
        try:
            write_retry(p.path)
        except (SyntaxError, FileNotFoundError) as e:
            print(f"⚠️  {p.rel}: 生成 {RETRY_NAME} 失败（{e}），请手动闭卷重写")
    print_selection(chosen, today, len(due), len(fill), sum(1 for p in problems if p.is_due(today)))
    print(f"\n✅ Today/ 已更新：{len(chosen)} 个软链接（顺序已随机打乱）→ 各题的文件夹，每题里有 {RETRY_NAME}（方法体已清空，闭卷重写用）")
    # ④ 可选：网站上的旧代码清空（--reset 才做，默认不做）
    if reset and chosen:
        reset_online(chosen)
    print('   做完一题: finish <序号> [g|y|r]')


# ---------------------------------------------------------------- note.md
def _append_note(p: Problem, section: str) -> Path:
    """往题目文件夹的 note.md 追加一段（文件不存在就建，带标题）。"""
    nf = p.path / NOTE_NAME
    if nf.exists():
        cur = nf.read_text(encoding="utf-8")
        sep = "" if cur.endswith("\n\n") else ("\n" if cur.endswith("\n") else "\n\n")
        nf.write_text(cur + sep + section.rstrip("\n") + "\n", encoding="utf-8")
    else:
        nf.write_text(f"# {p.title} 笔记\n\n" + section.rstrip("\n") + "\n", encoding="utf-8")
    return nf


def commented_classes(src: str) -> str | None:
    """取出源码里所有**带 # 注释**的顶层 class（含装饰器），原样拼接；一个都没有就返回 None。"""
    import ast, io, tokenize
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None
    lines = src.splitlines(keepends=True)
    blocks = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        start = min([node.lineno] + [d.lineno for d in node.decorator_list])
        seg = "".join(lines[start - 1:node.end_lineno])
        try:
            has_comment = any(t.type == tokenize.COMMENT for t in tokenize.generate_tokens(io.StringIO(seg).readline))
        except (tokenize.TokenError, IndentationError):
            has_comment = "#" in seg
        if has_comment:
            blocks.append(seg.rstrip("\n"))
    return "\n\n\n".join(blocks) if blocks else None


def archive_retry(p: Problem, today: date) -> None:
    """finish/done 删掉 solution_retry.py 之前：把里面带注释的 class 存进 note.md（"### 📝 日期 - retry N"）。"""
    rf = p.path / RETRY_NAME
    if not rf.exists():
        return
    code = commented_classes(rf.read_text(encoding="utf-8"))
    if not code:
        return
    block = f"```python\n{code}\n```"
    nf = p.path / NOTE_NAME
    existing = nf.read_text(encoding="utf-8") if nf.exists() else ""
    if block in existing:
        print(f"   📝 {RETRY_NAME} 里的注释已经在 {NOTE_NAME} 里了，不重复记")
        return
    n = existing.count("- retry ") + 1
    _append_note(p, f"### 📝 {today.isoformat()} - retry {n}\n\n{block}\n")
    print(f"   📝 {RETRY_NAME} 里带注释的 class 已存进 {NOTE_NAME}（retry {n}）")


def archive_comment(p: Problem, today: date, status: str, note: str) -> None:
    _append_note(p, f"### 💬 {today.isoformat()} - finish {status}\n\n{note.strip()}\n")
    print(f"   💬 评语已记进 {NOTE_NAME}")


def _remove_retry(link_or_dir: Path) -> None:
    try:
        target = link_or_dir.resolve()
        rf = target / RETRY_NAME
        if target.is_dir() and rf.exists():
            rf.unlink()
    except OSError:
        pass


def _record(p: Problem, status: str, note: str | None) -> None:
    st = STATUS_MAP.get(status.lower() if status.isascii() else status)
    if not st:
        sys.exit("状态只能是 g / y / r（或 🟢 🟡 🔴）")
    if p.graduated:
        sys.exit(f"这题已经毕业了：{p.rel}")
    p.practice.append({"date": date.today().isoformat(), "sticking_point": note or "", "result": st})
    p.save()
    lvl, grad = p.level()
    if grad:
        print(f"{st} 已记录 → {p.rel}\n   🎓 毕业！不再叫号（档案永远留在 metadata.json 里）")
    else:
        print(f"{st} 已记录 → {p.rel}\n   下次复习: {p.next_date.isoformat()}（{INTERVALS[lvl]} 天后）")
    if note:
        archive_comment(p, date.today(), st, note)
    from progress import update_progress      # 记完结果刷新 progress.md（shuffle 不刷新）
    update_progress()


def cmd_finish(which: str, status: str) -> None:
    """which 是数字 → Today/ 里的序号（老用法）；否则当作题目文件夹路径（绝对或相对当前目录）：
    文件夹必须存在、里面必须有 solution_retry.py，否则报错；做的事和序号用法完全一样，
    Today/ 里如果有指向它的软链接也一并移除。"""
    all_links = [e for e in TODAY_DIR.iterdir() if e.is_symlink()] if TODAY_DIR.is_dir() else []
    if which.isdigit():
        prefix = f"{int(which):02d} - "
        links = [e for e in all_links if e.name.startswith(prefix)]
        if not links:
            have = sorted(e.name for e in all_links)
            sys.exit(f"Today/ 里没有序号 {int(which)} 的题。" + ("现有：\n  " + "\n  ".join(have) if have else "Today/ 是空的，先 shuffle。"))
        link: Path | None = links[0]
        target = link.resolve()
    else:
        target = Path(which).expanduser().resolve()
        if not target.is_dir():
            sys.exit(f"❌ 文件夹不存在：{which}")
        if not (target / RETRY_NAME).exists():
            sys.exit(f"❌ {target} 里没有 {RETRY_NAME}（这题没在做，或者已经 finish 过了）")
        links = [e for e in all_links if e.resolve() == target]
        link = links[0] if links else None
    problems = load_all()
    hits = [x for x in problems if x.path == target]
    if not hits:
        sys.exit(f"这个文件夹不是题目（没有 metadata.json 或不在题库里）：{target}")
    archive_retry(hits[0], date.today())      # 先把 solution_retry.py 里的注释存进 note.md，再删它
    _record(hits[0], status, None)
    _remove_retry(target)
    if link is not None:
        link.unlink()
    left = sorted(e.name for e in TODAY_DIR.iterdir() if e.is_symlink()) if TODAY_DIR.is_dir() else []
    where = "已从 Today/ 移除" if link is not None else "（不在 Today/ 里）"
    print(f"   {where}，{RETRY_NAME} 已删" + (f"；Today/ 还剩 {len(left)} 题" if left else "；Today/ 已清空 🎉"))
    # 刚做完 Today/ 里的最后一题 → 自动再挑一批，省得手动 shuffle。
    # 只在"这次 finish 确实从 Today/ 拿掉了一题"时触发；本来就空着（按路径 finish 队列外的题）不打扰。
    if link is not None and not left:
        print(f"\n🔀 今天这批做完了，自动 shuffle {AUTO_SHUFFLE_N} 题：")
        cmd_shuffle(AUTO_SHUFFLE_N)


LC_ID_RE = re.compile(r"LC-\d{4}")
NC_REF_RE = re.compile(r"NC(?: - |%20-%20)")
ROW_RE = re.compile(r"^\s*(?:\||[-*+] |\d+\. )")      # markdown 表格行 / 列表项：整行删掉是安全的


def _to_trash(path: Path) -> str:
    """把路径移进 macOS 废纸篓（可恢复）。不用 rm：题库的 PDF 和图片被 gitignore，git 救不回来。"""
    if shutil.which("trash"):
        r = subprocess.run(["trash", str(path)], capture_output=True, text=True)
        if r.returncode == 0 and not path.exists():
            return "废纸篓"
        print(f"   ⚠️ trash 命令失败（{r.stderr.strip()[:80]}），改用手动搬运")
    dest_dir = Path.home() / ".Trash" / f"leetcode-removed-{date.today().isoformat()}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest, i = dest_dir / path.name, 2
    while dest.exists():
        dest = dest_dir / f"{path.name} ({i})"; i += 1
    shutil.move(str(path), str(dest))
    return str(dest)


def find_md_refs(folder_name: str, skip_under: Path | None = None) -> list[tuple[Path, int, str, bool]]:
    """在题库所有 .md 里找引用这个题目文件夹的行（README 的链接是百分号编码的，所以两种写法都要找）。
    skip_under：题目文件夹自己里面的 .md（note.md 之类）不算，它们跟着文件夹一起进废纸篓。
    返回 (md 文件, 行号, 行内容, 这一行是否只提到了这一道题)。"""
    forms = {folder_name, urllib.parse.quote(folder_name)}
    out = []
    for md in sorted(ROOT.rglob("*.md")):
        parts = md.relative_to(ROOT).parts
        if any(x in EXCLUDE_PARTS or x.startswith(("$$", ".")) for x in parts):
            continue
        if skip_under is not None and md.is_relative_to(skip_under):
            continue
        try:
            lines = md.read_text(encoding="utf-8").split("\n")
        except (OSError, UnicodeDecodeError):
            continue
        for i, line in enumerate(lines, 1):
            if not any(f in line for f in forms):
                continue
            markers = len(LC_ID_RE.findall(line)) + len(NC_REF_RE.findall(line))
            mine = sum(line.count(f) for f in forms)
            solo = markers <= mine and bool(ROW_RE.match(line))
            out.append((md, i, line, solo))
    return out


def prune_empty_parents(start: Path, dry: bool, ignore: Path | None = None) -> list[Path]:
    """题目删掉后，把因此空掉的子分类 / cluster 文件夹一起收走（大类文件夹保留）。
    ignore：预演时题目文件夹还在，要当它已经没了，否则会漏报。"""
    gone, d = [], start
    while len(d.relative_to(ROOT).parts) >= 2:            # 只收 ROOT 下第二层及更深的，不碰大类
        rest = [f for f in d.iterdir() if f.name != ".DS_Store" and f != ignore] if d.is_dir() else []
        if rest:
            break
        gone.append(d)
        if not dry:
            for junk in d.glob(".DS_Store"):
                junk.unlink()
            d.rmdir()
        d = d.parent
    return gone


def cmd_remove(which: str, dry: bool = False) -> None:
    """把一道题彻底从题库里剔除。which 是数字 → Today/ 里的序号；否则当作题目文件夹路径。"""
    all_links = [e for e in TODAY_DIR.iterdir() if e.is_symlink()] if TODAY_DIR.is_dir() else []
    if which.isdigit():
        prefix = f"{int(which):02d} - "
        links = [e for e in all_links if e.name.startswith(prefix)]
        if not links:
            have = sorted(e.name for e in all_links)
            sys.exit(f"Today/ 里没有序号 {int(which)} 的题。"
                     + ("现有：\n  " + "\n  ".join(have) if have else "Today/ 是空的，先 shuffle。"))
        link: Path | None = links[0]
        target = link.resolve()
    else:
        target = Path(which).expanduser().resolve()
        if not target.is_dir():
            sys.exit(f"❌ 文件夹不存在：{which}")
        links = [e for e in all_links if e.resolve() == target]
        link = links[0] if links else None

    # ---- 安全闸门：只允许删题库里的题目文件夹
    if not target.is_relative_to(ROOT):
        sys.exit(f"❌ 不在题库里，拒绝删除：{target}")
    if len(target.relative_to(ROOT).parts) < 2:
        sys.exit(f"❌ 这不是一道题（题目文件夹在 <大类>/<子分类>/ 下面），拒绝删除：{target.relative_to(ROOT)}")
    if not PROBLEM_DIR_RE.match(target.name):
        sys.exit(f"❌ 不是题目文件夹（名字要以 'LC-1234 - ' 或 'NC - ' 开头）：{target.name}")

    files = sorted(f for f in target.rglob("*") if f.is_file() and f.name != ".DS_Store")
    size = sum(f.stat().st_size for f in files)
    head = "【--dry-run，什么都不会动】" if dry else ""
    print(f"🗑  即将剔除{head}：{target.relative_to(ROOT)}")
    human = f"{size / 1024 / 1024:.1f} MB" if size >= 1024 * 1024 else (f"{size / 1024:.0f} KB" if size >= 1024 else f"{size} 字节")
    print(f"   {len(files)} 个文件，{human}")
    for f in files:
        print(f"      {f.relative_to(target)}")
    if not (target / "metadata.json").exists():
        print("   （这题没有 metadata.json，本来就不在复习队列里）")

    refs = find_md_refs(target.name, skip_under=target)
    solo = [r for r in refs if r[3]]
    manual = [r for r in refs if not r[3]]
    if refs:
        print(f"   README 引用：{len(refs)} 处（{len(solo)} 处可自动清掉，{len(manual)} 处需要你自己看一眼）")

    if dry:
        for md, i, line, ok in refs:
            print(f"      {'会删掉' if ok else '保留并提醒'} {md.relative_to(ROOT)}:{i}")
        will_go = [str(d.relative_to(ROOT)) for d in prune_empty_parents(target.parent, True, ignore=target)]
        print(f"   空掉的文件夹会一起收走：{will_go or '无'}")
        print("\n[--dry-run] 没有任何改动")
        return

    # ---- 真删
    where = _to_trash(target)
    print(f"   ✅ 题目文件夹已移进{where if where == '废纸篓' else '废纸篓：' + where}（可在 Finder 里还原）")
    if link is not None:
        link.unlink(); print("   ✅ Today/ 里的软链接已移除")
    for md, i, line, ok in sorted(solo, key=lambda r: (str(r[0]), -r[1])):   # 同一文件从后往前删，行号不乱
        if not md.exists():
            continue
        lines = md.read_text(encoding="utf-8").split("\n")
        del lines[i - 1]
        md.write_text("\n".join(lines), encoding="utf-8")
        print(f"   ✅ 已删掉引用行 {md.relative_to(ROOT)}:{i}")
    for md, i, line, ok in manual:
        print(f"   ⚠️ 这一行还提到别的题，没敢动，你自己看一眼：{md.relative_to(ROOT)}:{i}")
    for d in prune_empty_parents(target.parent, False):
        print(f"   ✅ 空掉的文件夹已收走：{d.relative_to(ROOT)}")

    from progress import update_progress
    update_progress()
    print("   ✅ progress.md 已刷新")
    left = sorted(e.name for e in TODAY_DIR.iterdir() if e.is_symlink()) if TODAY_DIR.is_dir() else []
    if link is not None:
        print(f"   Today/ 还剩 {len(left)} 题" if left else "   Today/ 已清空 🎉")
    if link is not None and not left:
        print(f"\n🔀 Today/ 空了，自动 shuffle {AUTO_SHUFFLE_N} 题：")
        cmd_shuffle(AUTO_SHUFFLE_N)


def cmd_done(target: str, status: str, note: str | None) -> None:
    problems = load_all()
    p = resolve(target, problems)
    archive_retry(p, date.today())
    _record(p, status, note)
    _remove_retry(p.path)


def cmd_stats() -> None:
    problems = load_all()
    today = date.today()
    due = [p for p in problems if p.is_due(today)]
    sched = [p for p in problems if p.next_date and not p.is_due(today)]
    unsch = [p for p in problems if p.unscheduled]
    grad = [p for p in problems if p.graduated]
    print(f"题目总数 {len(problems)} ｜ 到期 {len(due)} ｜ 已排期未到 {len(sched)} ｜ 未排期 {len(unsch)} ｜ 毕业 {len(grad)}")
    core = [p for p in problems if p.core]
    if core:
        c_in = [p for p in core if not p.unscheduled]
        c_green = [p for p in c_in if p.history[-1][1] == "🟢"]
        c_grad = [p for p in core if p.graduated]
        print(f"★ 核心层 NC150：在库 {len(core)} ｜ 已进入循环 {len(c_in)} ｜ 上次🟢 {len(c_green)} ｜ 毕业 {len(c_grad)}"
              f" ｜ 还没碰过 {len(core) - len(c_in)}   （tools/nc150.txt；shuffle 会先清它们）")
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
    fc = Counter(p.next_date for p in problems if p.next_date and p.next_date > today)
    row = " ｜ ".join(f"+{i}天 {fc.get(today + timedelta(days=i), 0)}" for i in range(1, 8))
    print(f"\n到期预测（今天积压 {len(due)} 之外，接下来 7 天各新到期多少）：{row}")
    leeches = [(sum(1 for _, st in p.history if st == "🔴"), p) for p in problems]
    leeches = sorted(((k, p) for k, p in leeches if k >= LEECH_REDS), key=lambda x: -x[0])
    if leeches:
        print(f"\n🩸 顽固题（累计 🔴 ≥ {LEECH_REDS}）：别再硬刷，先把解法读懂、拆成更小的模板再回来")
        for k, p in leeches[:10]:
            print(f"  🔴×{k}  {p.id}  {p.title}")
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
        "core": lambda p: p.core,
    }.get(which)
    if not sel:
        sys.exit("list 后面只能是 due | unscheduled | scheduled | graduated | all | core")
    rows = [p for p in problems if sel(p)]
    for p in rows:
        if p.graduated:
            state = "毕业 ✅"
        elif p.next_date:
            state = f"下次 {p.next_date.isoformat()}"
        else:
            state = "未排期"
        hist = " ".join(h[1] for h in p.history) or "-"
        print(f"{state:14s} {hist:8s} {'★' if p.core else ' '} {p.rel}")
    print(f"\n共 {len(rows)} 题")


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
    n_flag = _flag(rest, "-n")
    n = int(n_flag) if n_flag else SHUFFLE_N
    if cmd == "today":
        cmd_today(n)
    elif cmd == "shuffle":
        cmd_shuffle(n, reset="--reset" in rest)       # 默认不去网站重置代码；要重置就 --reset 或单独 `review reset`
    elif cmd == "reset":
        cmd_reset(int(rest[0]) if rest and rest[0].isdigit() else None)
    elif cmd == "mono":
        cmd_mono("--apply" in rest)
    elif cmd == "done":
        note = _flag(rest, "--note")
        if len(rest) != 2:
            sys.exit('用法: done <子串> <g|y|r> [--note "卡点"]')
        cmd_done(rest[0], rest[1], note)
    elif cmd == "finish":
        if not rest or len(rest) > 2:
            sys.exit('用法: finish <Today 里的序号 | 题目文件夹路径> [g|y|r]')
        cmd_finish(rest[0], rest[1] if len(rest) == 2 else "g")
    elif cmd == "remove":
        dry = "--dry-run" in rest
        rest = [x for x in rest if x != "--dry-run"]
        if len(rest) != 1:
            sys.exit("用法: remove <Today 里的序号 | 题目文件夹路径> [--dry-run]")
        cmd_remove(rest[0], dry)
    elif cmd == "stats":
        cmd_stats()
    elif cmd == "list":
        cmd_list(rest[0] if rest else "due")
    else:
        sys.exit(f"未知命令: {cmd}\n\n{__doc__.strip()}")


if __name__ == "__main__":
    main(sys.argv[1:])
