#!/usr/bin/env python3
"""
progress.py — 生成根目录 progress.md（进度的唯一来源）

只在 intake（入库）和 finish / done（记结果）时刷新；shuffle 不刷新。
手动刷新：python3 tools/progress.py

progress.md 末尾带一个 ```json 块，macOS 悬浮窗小组件（tuto_mac_os_widgets/ProgressWidget）就读它。
"""
from __future__ import annotations
import json, sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from review_due import load_all, Problem, INTERVALS, ROOT  # noqa: E402

OUT = ROOT / "progress.md"
DIFF_NAME = {"E": "Easy", "M": "Medium", "H": "Hard"}


def pct(a: int, b: int) -> float:
    return round(100.0 * a / b, 1) if b else 0.0


def compute(problems: list[Problem], today: date) -> dict:
    total = len(problems)
    grad = [p for p in problems if p.graduated]
    unsch = [p for p in problems if p.unscheduled]
    inrev = [p for p in problems if not p.unscheduled and not p.graduated]
    due = [p for p in problems if p.is_due(today)]

    diff = Counter((p.meta.get("difficulty") or "?") for p in problems)
    by_diff = {k: {"count": diff.get(k, 0), "pct": pct(diff.get(k, 0), total)} for k in ("E", "M", "H")}
    if diff.get("?"):
        by_diff["?"] = {"count": diff["?"], "pct": pct(diff["?"], total)}

    # 复习中的题处在哪一级（下次间隔 1/3/7/14/30 天）
    levels = Counter(INTERVALS[p.level()[0]] for p in inrev)
    by_level = {str(d): levels.get(d, 0) for d in INTERVALS}

    # 所有复习记录
    results = Counter()
    per_day: Counter = Counter()
    for p in problems:
        for d, st in p.history:
            results[st] += 1
            per_day[d] += 1
    n_reviews = sum(results.values())
    last7 = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    week = [{"date": d.isoformat(), "count": per_day.get(d, 0)} for d in last7]
    streak = 0
    d = today if per_day.get(today) else today - timedelta(days=1)
    while per_day.get(d):
        streak += 1
        d -= timedelta(days=1)
    last_review = max(per_day) if per_day else None

    # 按大类
    cats: dict[str, dict] = {}
    for p in problems:
        c = cats.setdefault(p.category, {"total": 0, "graduated": 0, "in_review": 0, "unscheduled": 0, "due": 0})
        c["total"] += 1
        if p.graduated:
            c["graduated"] += 1
        elif p.unscheduled:
            c["unscheduled"] += 1
        else:
            c["in_review"] += 1
        if p.is_due(today):
            c["due"] += 1
    for c in cats.values():
        c["pct"] = pct(c["graduated"], c["total"])
        c["started_pct"] = pct(c["graduated"] + c["in_review"], c["total"])

    # 毕业的题按难度
    grad_diff = Counter((p.meta.get("difficulty") or "?") for p in grad)

    return {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "by_difficulty": by_diff,
        "graduated": {"count": len(grad), "pct": pct(len(grad), total),
                      "by_difficulty": {k: grad_diff.get(k, 0) for k in ("E", "M", "H")}},
        "in_review": {"count": len(inrev), "pct": pct(len(inrev), total)},
        "started": {"count": len(inrev) + len(grad), "pct": pct(len(inrev) + len(grad), total)},
        "unscheduled": {"count": len(unsch), "pct": pct(len(unsch), total)},
        "due_today": len(due),
        "progress_pct": pct(len(grad), total),
        "by_level": by_level,
        "reviews": {"total": n_reviews, "green": results.get("🟢", 0), "yellow": results.get("🟡", 0),
                    "red": results.get("🔴", 0), "green_pct": pct(results.get("🟢", 0), n_reviews)},
        "week": week,
        "streak_days": streak,
        "last_review": last_review.isoformat() if last_review else None,
        "by_category": [{"name": k, **v} for k, v in sorted(cats.items())],
    }


def bar(p: float, width: int = 30) -> str:
    full = int(round(width * p / 100))
    return "█" * full + "░" * (width - full)


def render(s: dict) -> str:
    L: list[str] = []
    L.append("# 复习进度\n")
    L.append(f"> 自动生成，最后更新 {s['updated']}。只在 intake / finish / done 时刷新；手动刷新：`python3 tools/progress.py`。\n")
    L.append(f"## 总进度：{s['progress_pct']}%\n")
    L.append(f"`{bar(s['progress_pct'])}`  {s['graduated']['count']} / {s['total']} 题毕业\n")
    L.append("毕业 = 间隔 1 → 3 → 7 → 14 → 30 天连续 5 个 🟢。\n")

    L.append("## 题库\n")
    L.append("| | 数量 | 占比 |\n|---|---:|---:|")
    L.append(f"| 总题数 | {s['total']} | 100% |")
    for k in ("E", "M", "H", "?"):
        if k in s["by_difficulty"]:
            v = s["by_difficulty"][k]
            L.append(f"| {DIFF_NAME.get(k, '未知难度')} | {v['count']} | {v['pct']}% |")
    L.append("")

    L.append("## 复习状态\n")
    g, r, u, st = s["graduated"], s["in_review"], s["unscheduled"], s["started"]
    L.append("| 状态 | 数量 | 占总题数 |\n|---|---:|---:|")
    L.append(f"| 🎓 已毕业 | {g['count']} | {g['pct']}% |")
    L.append(f"| 🔁 复习中（至少复习过一次，未毕业） | {r['count']} | {r['pct']}% |")
    L.append(f"| 🚀 已进入复习（复习中 + 毕业） | {st['count']} | {st['pct']}% |")
    L.append(f"| 💤 还没开始复习 | {u['count']} | {u['pct']}% |")
    L.append(f"| ⏰ 今天到期 | {s['due_today']} | |")
    L.append("")
    gd = g["by_difficulty"]
    L.append(f"毕业的题按难度：Easy {gd['E']} · Medium {gd['M']} · Hard {gd['H']}\n")

    L.append("## 复习中的题处在哪一级\n")
    L.append("| 下次间隔 | " + " | ".join(f"{d} 天" for d in INTERVALS) + " |")
    L.append("|---|" + "---:|" * len(INTERVALS))
    L.append("| 题数 | " + " | ".join(str(s["by_level"][str(d)]) for d in INTERVALS) + " |")
    L.append("")

    rv = s["reviews"]
    L.append("## 复习记录\n")
    L.append(f"- 累计复习 {rv['total']} 次：🟢 {rv['green']} · 🟡 {rv['yellow']} · 🔴 {rv['red']}（🟢 率 {rv['green_pct']}%）")
    L.append(f"- 连续复习 {s['streak_days']} 天" + (f"，最近一次 {s['last_review']}" if s["last_review"] else ""))
    L.append("- 最近 7 天：" + "  ".join(f"{w['date'][5:]} {w['count']}" for w in s["week"]))
    L.append("")

    L.append("## 按大类\n")
    L.append("| 大类 | 总数 | 毕业 | 复习中 | 未开始 | 今天到期 | 毕业率 | 已进入复习 |\n|---|---:|---:|---:|---:|---:|---:|---:|")
    for c in s["by_category"]:
        L.append(f"| {c['name']} | {c['total']} | {c['graduated']} | {c['in_review']} | {c['unscheduled']} | {c['due']} | {c['pct']}% | {c['started_pct']}% |")
    L.append("")

    L.append("## 机器可读（小组件读这一段）\n")
    L.append("```json")
    L.append(json.dumps(s, ensure_ascii=False, indent=2))
    L.append("```")
    return "\n".join(L) + "\n"


def update_progress(quiet: bool = False) -> Path:
    s = compute(load_all(), date.today())
    OUT.write_text(render(s), encoding="utf-8")
    if not quiet:
        print(f"📈 progress.md 已更新：毕业 {s['graduated']['count']}/{s['total']}（{s['progress_pct']}%）"
              f"，复习中 {s['in_review']['count']}，未开始 {s['unscheduled']['count']}，今天到期 {s['due_today']}")
    return OUT


if __name__ == "__main__":
    update_progress()
