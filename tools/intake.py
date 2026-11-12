#!/usr/bin/env python3
"""
intake.py — 把 New/ 里的新题入库（只依赖标准库；抓题面 PDF 时调用 tuto_etsy 的 puppeteer 脚本）

前提（任一不满足就报错退出，什么都不改）：
    1. New/ 里有且只有一个 .py，且名字是 solution.py
    2. solution.py 第一行是注释形式的题目链接：
         # https://leetcode.com/problems/repeated-dna-sequences/description/
         # https://neetcode.io/problems/k-closest-points-to-origin/question?list=neetcode150
       由链接自动判断是 LeetCode 还是 NeetCode 题

用法：
    python3 tools/intake.py --dry-run                      只解析并打印将要做什么（不需要 --target）
    python3 tools/intake.py --target "<大类>/<子分类>" [--no-pdf]

    模式二（题已经自己归好类，只缺文件）：
    python3 tools/intake.py "<.../LC-3291 - xxx/solution.py>" [更多路径...] [--no-pdf] [--force]
        给传进来的题目文件夹补齐 metadata.json / problem.pdf / problem_dark.pdf，文件夹**原地不动**；
        已存在的文件默认不覆盖（--force 才覆盖）；传 cluster / 子分类文件夹时，里面所有带 solution.py 的题一起补。
        链接来源：solution.py 第一行的 `# <链接>`（会被移除），没有就用文件夹名里的 LC-编号 / NC 标题反查。

做的事：
    <target>/LC-0187 - Repeated DNA Sequences/   （NeetCode 题是 NC - <标题>/）
        solution.py     ← New/solution.py 去掉第一行链接注释
        metadata.json   ← id / path（相对仓库根目录）/ difficulty / link / practice
                          （题目标题、信号→模式都不进 metadata，全靠文件夹名：LC-0187 - Title - <信号/备注>）
        problem.pdf     ← 从 LeetCode / NeetCode 抓取的题面
        note.md         ← New/note.md（有才有；这道题今后所有文字笔记都在这里）
        asset-*.…       ← New/ 里其他所有文件（图片、PDF…），直接放这一层，加 asset- 前缀，不再建 assets/ 子文件夹
    然后清空 New/。
"""
from __future__ import annotations
import json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEW = ROOT / "New"
ETSY = Path("/Users/bohaoli/Desktop/tuto/tuto_etsy")
QUESTION_LIST = ETSY / "VV-utils/question_list.json"
NC_TITLES = ETSY / "VV-utils/data/neetcode-titles.json"
LC_PDF_SCRIPT = "VV-utils/01-leetcode-question.ts"
NC_PDF_SCRIPT = "VV-utils/09-generate-neetcode-links.ts"
EMOJI = re.compile(r"[\U0001F000-\U0001FFFF☀-➿⬀-⯿️⃣←-⇿⌀-⏿]")


def die(msg: str) -> None:
    sys.exit(f"❌ {msg}")


def clean_name(name: str) -> str:
    stem, ext = os.path.splitext(name)
    s = EMOJI.sub("", stem).replace("|", "、")
    s = re.sub(r"(\s*-\s*){2,}", " - ", s)
    s = re.sub(r"\s+", " ", s).strip(" -")
    return (s or stem) + ext


def sanitize_title(t: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[/\\:*?\"<>|]", " ", t)).strip()


# ---------------------------------------------------------------- 1. 校验 New/
def read_new() -> tuple[Path, str, list[Path]]:
    if not NEW.is_dir():
        die(f"没有 New/ 文件夹：{NEW}")
    entries = [p for p in NEW.iterdir() if not p.name.startswith(".")]
    pys = [p for p in entries if p.suffix == ".py"]
    if len(pys) != 1:
        die(f"New/ 里必须有且只有一个 .py 文件，现在有 {len(pys)} 个：{[p.name for p in pys]}")
    if pys[0].name != "solution.py":
        die(f"New/ 里的 python 文件必须叫 solution.py，现在是 {pys[0].name}")
    src = pys[0]
    first = src.read_text(encoding="utf-8").split("\n", 1)[0].strip()
    m = re.match(r"^#\s*(https?://\S+)\s*$", first)
    if not m:
        die(f"solution.py 第一行必须是 '# <题目链接>'，现在是：{first!r}")
    others = [p for p in entries if p != src]
    return src, m.group(1), others


# ---------------------------------------------------------------- 2. 解析链接
def parse_link(url: str) -> dict:
    m = re.match(r"^https?://(?:www\.)?leetcode\.(?:com|cn)/problems/([^/?#]+)", url)
    if m:
        slug = m.group(1)
        entry = next((p for p in json.load(open(QUESTION_LIST))["stat_status_pairs"] if p["stat"]["question__title_slug"] == slug), None)
        if not entry:
            die(f"question_list.json 里找不到 slug={slug}（题单可能过期，需要更新 tuto_etsy/VV-utils/question_list.json）")
        qid = entry["stat"]["frontend_question_id"]
        title = entry["stat"]["question__title"]
        diff = {1: "E", 2: "M", 3: "H"}.get(entry["difficulty"]["level"])
        nc = json.load(open(NC_TITLES)) if NC_TITLES.exists() else []
        nc_hit = next((e for e in nc if e["title"].lower() == title.lower()), None)
        return {"kind": "LC", "id": f"LC-{qid:04d}", "folder": f"LC-{qid:04d} - {sanitize_title(title)}", "title": title, "difficulty": diff,
                "link": {"leetcode": f"https://leetcode.com/problems/{slug}/", "neetcode": nc_hit["url"] if nc_hit else None}, "url": url}
    m = re.match(r"^https?://(?:www\.)?neetcode\.io/problems/([^/?#]+)", url)
    if m:
        slug = m.group(1)
        nc = json.load(open(NC_TITLES)) if NC_TITLES.exists() else []
        hit = next((e for e in nc if e["slug"] == slug), None)
        if not hit:
            die(f"neetcode-titles.json 里找不到 slug={slug}（不在 NeetCode 150 里？可先用 tuto_etsy 的 10-fetch-neetcode-titles.ts 补抓）")
        title = hit["title"]
        lc = next((p for p in json.load(open(QUESTION_LIST))["stat_status_pairs"] if p["stat"]["question__title"].lower() == title.lower()), None)
        return {"kind": "NC", "id": f"NC-{slug}", "folder": f"NC - {sanitize_title(title)}", "title": title, "difficulty": (hit.get("difficulty") or "")[:1] or None,
                "link": {"leetcode": f"https://leetcode.com/problems/{lc['stat']['question__title_slug']}/" if lc else None, "neetcode": hit["url"]}, "url": url}
    die(f"链接既不是 leetcode.com/problems/… 也不是 neetcode.io/problems/…：{url}")


# ---------------------------------------------------------------- 3. 题面 PDF
def run_tsx(args: list[str]) -> str:
    r = subprocess.run(["npx", "tsx", *args], cwd=ETSY, capture_output=True, text=True)
    return (r.stdout or "") + (r.stderr or "")


def fetch_pdf(info: dict, dest: Path) -> bool:
    try:
        if info["kind"] == "LC":
            out = run_tsx([LC_PDF_SCRIPT, info["link"]["leetcode"]])
            m = re.search(r"PDF generated successfully at (.*)\.\s*$", out, re.M)
            if not m:
                print("  ⚠️ 题面抓取失败（LeetCode）：\n" + out[-600:]); return False
            shutil.move(m.group(1), dest); return True
        with tempfile.TemporaryDirectory() as tmp:
            stub = Path(tmp) / f"01 - {sanitize_title(info['title'])}.py"
            stub.write_text("", encoding="utf-8")
            out = run_tsx([NC_PDF_SCRIPT, str(stub), info["url"]])
            pdfs = list(Path(tmp).glob("01 - ⭐️ - *.pdf"))
            if not pdfs:
                print("  ⚠️ 题面抓取失败（NeetCode）：\n" + out[-600:]); return False
            shutil.move(str(pdfs[0]), dest); return True
    except Exception as e:  # noqa: BLE001
        print(f"  ⚠️ 题面抓取异常：{e}"); return False


# ---------------------------------------------------------------- 4. 入库
def list_targets() -> None:
    """列出所有可以当 --target 的子分类（递归：11-graphs 这种大类下面是 <阶段>/<模板> 两级）。"""
    print('请用 --target 指定目标子分类（可以多级，例如 "11-graphs (图论)/02-dfs-bfs (阶段 1 · …)/flood-fill (洪水填充：数连通块)"）。现有的大类 / 子分类：')
    skip = {"utils", "docs (资料)", "tutorials (教程)", "templates (模板)", "__pycache__"}

    def walk(d: Path, depth: int) -> None:
        for s in sorted(x for x in d.iterdir() if x.is_dir()):
            if PROBLEM_DIR_RE.match(s.name) or s.name in skip or s.name.startswith((".", "$$", "00 - ", "00-")):
                continue              # 题目文件夹 / 工具 / 理论资料 不是归类目标
            print("    " * depth + s.name)
            walk(s, depth + 1)

    for big in sorted(p for p in ROOT.iterdir() if p.is_dir() and re.match(r"^\d\d-", p.name)):
        print(f"  {big.name}")
        walk(big, 2)


PROBLEM_DIR_RE = re.compile(r"^(?:\d{1,2} *- *)?(LC-\d{4}|NC) - ")   # 可选的数字优先级前缀，两种写法都认：01-LC-0876 - Title / 01 - LC-0743 - Title


def finish_files(folder: Path, no_pdf: bool = False, force: bool = False) -> None:
    """给一个已经放好位置、只有 solution.py 的题目文件夹补齐 metadata.json / problem.pdf / problem_dark.pdf。
    文件夹不动（位置是用户自己归的类），已存在的文件默认不覆盖（--force 才覆盖）。"""
    sol = folder / "solution.py"
    if not sol.exists():
        die(f"{folder} 里没有 solution.py")
    try:
        rel = folder.relative_to(ROOT)
    except ValueError:
        die(f"不在题库里：{folder}")
    if not PROBLEM_DIR_RE.match(folder.name):
        die(f"文件夹名必须以 'LC-1234 - ' 或 'NC - ' 开头，现在是：{folder.name}\n"
            f"（复习调度器靠这个前缀识别题目文件夹，改名后再跑）")

    # 链接：优先取 solution.py 第一行的注释；没有就从文件夹名里的编号反查
    body = sol.read_text(encoding="utf-8")
    first = body.split("\n", 1)[0].strip()
    m = re.match(r"^#\s*(https?://\S+)\s*$", first)
    if m:
        url = m.group(1)
    else:
        url = url_from_folder_name(folder.name)
        if not url:
            die(f"{folder.name}/solution.py 第一行不是题目链接，也没法从文件夹名反查到题目：{first!r}")
    info = parse_link(url)
    print(f"📁 {rel}")
    print(f"   {info['kind']}  {info['id']}  {info['title']}  (难度 {info['difficulty'] or '?'})")
    if m:                                   # 和 New/ 流程一致：链接注释搬进 metadata 后从代码里去掉
        sol.write_text(body.split("\n", 1)[1].lstrip("\n") if "\n" in body else "", encoding="utf-8")
        print("   solution.py 第一行的链接注释已移除 ✓")

    meta_f = folder / "metadata.json"
    if meta_f.exists() and not force:
        print("   metadata.json 已存在，跳过（--force 覆盖）")
    else:
        meta = {
            "id": info["id"], "path": str(rel),
            "difficulty": info["difficulty"], "link": info["link"],
            "practice": [],
        }
        meta_f.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("   metadata.json ✓")

    pdf = folder / "problem.pdf"
    if pdf.exists() and not force:
        print("   problem.pdf 已存在，跳过")
    elif no_pdf:
        print("   problem.pdf 跳过（--no-pdf）")
    else:
        print("   problem.pdf 抓取中…", flush=True)
        print("   problem.pdf " + ("✓" if fetch_pdf(info, pdf) else "✗（稍后可重抓）"))
    make_dark(pdf, force)


def url_from_folder_name(name: str) -> str | None:
    """从 'LC-3291 - xxx' / 'NC - xxx' 这样的文件夹名反查题目链接。"""
    m = re.match(r"^(?:\d{1,2} *- *)?LC-(\d{4}) - ", name)
    if m:
        qid = int(m.group(1))
        e = next((p for p in json.load(open(QUESTION_LIST))["stat_status_pairs"]
                  if p["stat"]["frontend_question_id"] == qid), None)
        return f"https://leetcode.com/problems/{e['stat']['question__title_slug']}/" if e else None
    nc_m = re.match(r"^(?:\d{1,2} *- *)?NC - ", name)
    if nc_m and NC_TITLES.exists():
        rest = name[nc_m.end():].strip()
        nc = json.load(open(NC_TITLES))
        # 文件夹名可以是 "NC - Title" 或 "NC - Title - <信号/备注>"：先整段匹配，不行再只取第一段
        for cand in (rest, rest.split(" - ", 1)[0].strip()):
            e = next((x for x in nc if x["title"].lower() == cand.lower()), None)
            if e:
                return e["url"]
        return None
    return None


def make_dark(pdf: Path, force: bool = False) -> None:
    if not pdf.exists():
        return
    dark = pdf.with_name("problem_dark.pdf")
    if dark.exists() and not force:
        print("   problem_dark.pdf 已存在，跳过"); return
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from pdf_dark import darken
        darken(pdf, dark); print("   problem_dark.pdf ✓")
    except Exception as e:  # noqa: BLE001
        print(f"   ⚠️ problem_dark.pdf 生成失败：{e}")


def cmd_existing(targets: list[str], no_pdf: bool, force: bool) -> None:
    folders: list[Path] = []
    for t in targets:
        p = Path(t).expanduser().resolve()
        if p.is_file():
            if p.name != "solution.py":
                die(f"只能传 solution.py 或题目文件夹，现在是：{p.name}")
            p = p.parent
        if not p.is_dir():
            die(f"路径不存在：{t}")
        if (p / "solution.py").exists():
            folders.append(p)
        else:   # 传的是 cluster / 子分类文件夹 → 把里面所有还缺 metadata 的题都补上
            subs = sorted(d for d in p.iterdir() if d.is_dir() and (d / "solution.py").exists())
            if not subs:
                die(f"{p} 里既没有 solution.py，也没有带 solution.py 的子文件夹")
            folders += subs
    for i, d in enumerate(folders):
        if i:
            print()
        finish_files(d, no_pdf, force)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from progress import update_progress
    update_progress()


def main(argv: list[str]) -> None:
    def flag(name):
        if name in argv:
            i = argv.index(name); v = argv[i + 1] if i + 1 < len(argv) else None
            if v is None: die(f"{name} 后面需要一个值")
            del argv[i:i + 2]; return v
        return None
    dry = "--dry-run" in argv; no_pdf = "--no-pdf" in argv; force = "--force" in argv
    target = flag("--target")

    # 模式二：题已经自己归好类了，只是缺文件 —— 把路径直接给过来，补全 metadata / problem.pdf / problem_dark.pdf
    existing = [a for a in argv if not a.startswith("--")]   # argv 已经不含脚本名
    if "--existing" in argv or existing:
        if not existing:
            die('用法: intake.py --existing "<题目文件夹或其 solution.py 的路径>" [...]')
        cmd_existing(existing, no_pdf, force); return

    src, url, others = read_new()
    info = parse_link(url)
    print(f"📥 New/solution.py → {info['kind']}  {info['id']}  {info['title']}  (难度 {info['difficulty'] or '?'})")
    print(f"   leetcode: {info['link']['leetcode']}\n   neetcode: {info['link']['neetcode']}")
    if others:
        print(f"   附带文件 → asset-*: {[p.name for p in others]}")
    if not target:
        print(); list_targets(); sys.exit(2)
    # 单调栈 / 单调队列相关的题一律强制归到 MONO_CAT（不管 --target 给的是什么）
    MONO_CAT = "18-monotonic-fuck-you (单调栈、单调队列)"
    MONO_RE = re.compile(r"monotonic|单调(栈|队列|递增栈|递减栈|双端)", re.I)
    mono_text = info["title"] + "\n" + src.read_text(encoding="utf-8")
    if MONO_RE.search(mono_text) and not target.startswith(MONO_CAT):
        (ROOT / MONO_CAT / "general").mkdir(parents=True, exist_ok=True)
        print(f"📦 这题和单调栈/单调队列沾边，强制归到 {MONO_CAT}/general（忽略 --target {target!r}）")
        target = f"{MONO_CAT}/general"
    target_dir = ROOT / target
    if not target_dir.is_dir():
        die(f"目标子分类不存在：{target_dir}\n（如需新建子分类，先 mkdir 再入库，命名风格 kebab-case (中文)）")
    dest = target_dir / info["folder"]
    if dest.exists():
        die(f"已经存在同名题目文件夹：{dest.relative_to(ROOT)}")
    print(f"   目标: {dest.relative_to(ROOT)}")
    if dry:
        print("\n[dry-run] 未做任何改动"); return

    dest.mkdir(parents=True)
    body = src.read_text(encoding="utf-8").split("\n", 1)[1] if "\n" in src.read_text(encoding="utf-8") else ""
    (dest / "solution.py").write_text(body.lstrip("\n"), encoding="utf-8")
    meta = {
        "id": info["id"], "path": str(dest.relative_to(ROOT)),
        "difficulty": info["difficulty"], "link": info["link"],
        "practice": [],
    }
    (dest / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    note_src = next((p for p in others if p.name.lower() == "note.md"), None)   # New/note.md → 题目文件夹根目录的 note.md
    if note_src:
        shutil.move(str(note_src), dest / "note.md"); others = [p for p in others if p is not note_src]
    if others:
        for p in others:
            n = clean_name(p.name)
            shutil.move(str(p), dest / (n if n.startswith("asset-") else "asset-" + n))
    ok = True if no_pdf else fetch_pdf(info, dest / "problem.pdf")
    src.unlink()
    print(f"\n✅ 已入库：{dest.relative_to(ROOT)}")
    print(f"   solution.py ✓   metadata.json ✓   problem.pdf {'✓' if ok and not no_pdf else '✗（稍后可重抓）'}   asset-* {'✓ ' + str(len(others)) + ' 个文件' if others else '—'}")
    print(f"   New/ 已清空 ｜ 记录复习: python3 tools/review_due.py done \"{info['folder']}\" <g|y|r>")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    if (dest / "problem.pdf").exists():
        try:
            from pdf_dark import darken           # 夜间版 problem_dark.pdf
            darken(dest / "problem.pdf", dest / "problem_dark.pdf")
            print("   problem_dark.pdf ✓")
        except Exception as e:  # noqa: BLE001
            print(f"   ⚠️ problem_dark.pdf 生成失败：{e}（可稍后 python3 tools/pdf_dark.py \"{dest / 'problem.pdf'}\"）")
    from progress import update_progress      # 入库后刷新 progress.md
    update_progress()


if __name__ == "__main__":
    main(sys.argv[1:])
