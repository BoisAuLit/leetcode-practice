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
    python3 tools/intake.py --target "<大类>/<子分类>" [--signal "信号 → 模式"] [--guard "..."] [--sticking "..."] [--no-pdf]

做的事：
    <target>/LC-0187 - Repeated DNA Sequences/   （NeetCode 题是 NC - <标题>/）
        solution.py     ← New/solution.py 去掉第一行链接注释
        metadata.json   ← id / title / difficulty / link / info / practice
        problem.pdf     ← 从 LeetCode / NeetCode 抓取的题面
        assets/         ← New/ 里其他所有文件（图片、笔记 PDF、md…），有才建
    然后清空 New/。
"""
from __future__ import annotations
import json, os, re, shutil, subprocess, sys, tempfile
from datetime import date
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
    print("请用 --target 指定目标子分类。现有的大类 / 子分类：")
    for big in sorted(p for p in ROOT.iterdir() if p.is_dir() and re.match(r"^\d\d-", p.name)):
        subs = sorted(d.name for d in big.iterdir() if d.is_dir() and not re.match(r"^(LC-\d{4}|NC) - ", d.name) and d.name not in ("utils", "docs (资料)"))
        print(f"  {big.name}")
        for s in subs:
            print(f"      {s}")


def main(argv: list[str]) -> None:
    def flag(name):
        if name in argv:
            i = argv.index(name); v = argv[i + 1] if i + 1 < len(argv) else None
            if v is None: die(f"{name} 后面需要一个值")
            del argv[i:i + 2]; return v
        return None
    dry = "--dry-run" in argv; no_pdf = "--no-pdf" in argv
    target = flag("--target"); signal = flag("--signal"); guard = flag("--guard"); sticking = flag("--sticking")

    src, url, others = read_new()
    info = parse_link(url)
    print(f"📥 New/solution.py → {info['kind']}  {info['id']}  {info['title']}  (难度 {info['difficulty'] or '?'})")
    print(f"   leetcode: {info['link']['leetcode']}\n   neetcode: {info['link']['neetcode']}")
    if others:
        print(f"   附带文件 → assets/: {[p.name for p in others]}")
    if not target:
        print(); list_targets(); sys.exit(2)
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
    sig, mode = (None, None)
    if signal:
        sig, mode = ([x.strip() for x in signal.split("→", 1)] + [None])[:2] if "→" in signal else (signal.strip(), None)
    meta = {
        "id": info["id"], "title": info["title"], "difficulty": info["difficulty"], "link": info["link"],
        "info": {"signal": sig, "mode": mode, "guard": guard, "sticking_point": sticking, "first_date": date.today().isoformat()},
        "practice": [],
    }
    (dest / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if others:
        (dest / "assets").mkdir()
        for p in others:
            shutil.move(str(p), dest / "assets" / clean_name(p.name))
    ok = True if no_pdf else fetch_pdf(info, dest / "problem.pdf")
    src.unlink()
    print(f"\n✅ 已入库：{dest.relative_to(ROOT)}")
    print(f"   solution.py ✓   metadata.json ✓   problem.pdf {'✓' if ok and not no_pdf else '✗（稍后可重抓）'}   assets/ {'✓ ' + str(len(others)) + ' 个文件' if others else '—'}")
    print(f"   New/ 已清空 ｜ 记录复习: python3 tools/review_due.py done \"{info['folder']}\" <g|y|r>")


if __name__ == "__main__":
    main(sys.argv[1:])
