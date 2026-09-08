#!/usr/bin/env python3
"""
add_headers_once.py — 一次性给已有解答文件批量加"复习头"（幂等，可重复运行）

    python3 tools/add_headers_once.py --dry-run   # 只检查：哪些路径找不到、哪些会被加头
    python3 tools/add_headers_once.py             # 真正写入
    python3 tools/add_headers_once.py --undo      # 精确移除本脚本加的、尚未使用过的头

数据源：tools/signals_manifest.txt，每行 "相对路径 ||| 信号→模式"。
首次日期：取该文件在 git 里第一次被添加的日期；不在 git 里则取文件修改日期。
已经有复习头（前 15 行含 "📌 信号→模式:"）的文件会被跳过，所以重复运行是安全的。
"""

from __future__ import annotations

import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = Path(__file__).resolve().parent / "signals_manifest.txt"
SEP = " ||| "


def has_header(p: Path) -> bool:
    try:
        with open(p, encoding="utf-8") as f:
            return any("📌 信号→模式:" in line for _, line in zip(range(15), f))
    except (UnicodeDecodeError, OSError):
        return False


def first_date(p: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--follow", "--format=%as", "--", str(p)],
            cwd=ROOT, capture_output=True, text=True, check=False,
        ).stdout.strip().splitlines()
        if out:
            return out[-1]  # 最早的一次添加
    except FileNotFoundError:
        pass
    return datetime.fromtimestamp(p.stat().st_mtime).date().isoformat()


def load_manifest() -> list[tuple[str, str]]:
    rows = []
    for raw in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if SEP not in line:
            print(f"⚠️  忽略格式错误的行: {line[:60]}")
            continue
        rel, signal = (s.strip() for s in line.split(SEP, 1))
        rows.append((rel, signal))
    return rows


def undo() -> None:
    """只移除本脚本加的、且从未被复习过的原始头（第 4 行仍是"未排期"）。不碰任何其他内容。"""
    removed = 0
    for rel, _ in load_manifest():
        p = ROOT / rel
        if not p.exists():
            continue
        lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
        if (
            len(lines) >= 5
            and lines[0].strip() == '"""'
            and "📌 信号→模式:" in lines[1]
            and "📅 首次:" in lines[2]
            and lines[3].strip() == "🔁 复习: 未排期"
            and lines[4].strip() == '"""'
        ):
            p.write_text("".join(lines[5:]), encoding="utf-8")
            removed += 1
    print(f"已移除 {removed} 个未使用过的复习头。")


def main(dry_run: bool) -> None:
    rows = load_manifest()
    missing, skipped, todo = [], [], []
    for rel, signal in rows:
        p = ROOT / rel
        if not p.exists():
            missing.append(rel)
        elif has_header(p):
            skipped.append(rel)
        else:
            todo.append((p, rel, signal))

    print(f"清单 {len(rows)} 条 ｜ 找不到 {len(missing)} ｜ 已有头跳过 {len(skipped)} ｜ 待加头 {len(todo)}")
    for rel in missing:
        print(f"  ❌ 找不到: {rel}")
    if missing and not dry_run:
        sys.exit("\n有路径找不到，先修正清单再运行（本次未写入任何文件）。")
    if dry_run:
        for _, rel, _ in todo[:10]:
            print(f"  ✍️  将加头: {rel}")
        if len(todo) > 10:
            print(f"  ... 共 {len(todo)} 个")
        return

    for p, rel, signal in todo:
        header = (
            '"""\n'
            f"📌 信号→模式: {signal}\n"
            f"📅 首次: {first_date(p)} | 卡点: （待补） | 守卫: （待补）\n"
            "🔁 复习: 未排期\n"
            '"""\n'
        )
        content = p.read_text(encoding="utf-8")
        p.write_text(header + content, encoding="utf-8")
        print(f"  ✅ {rel}")
    print(f"\n完成：新增复习头 {len(todo)} 个。用 git diff 检查；不满意运行 --undo 精确移除（不影响其他改动）。")


if __name__ == "__main__":
    if "--undo" in sys.argv:
        undo()
    else:
        main(dry_run="--dry-run" in sys.argv)
