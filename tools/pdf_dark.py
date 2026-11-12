#!/usr/bin/env python3
"""
pdf_dark.py — 把 problem.pdf 变成夜间版（颜色反转），不动字体、不栅格化，文字仍可选可搜。

原理：在每一页内容流末尾追加几个覆盖整页的矩形（页面原有内容一个字节都不改）：
    ① 白色 + Difference    结果 = |底色 − 白| = 1 − 底色   ⇒ 白底变黑、黑字变白、彩色取补色
    ② BOOST 灰 + ColorDodge 结果 = 底色 / (1 − BOOST)：亮的更亮（灰字 → 白），黑的还是黑（默认 0.35 ⇒ ×1.54）
    ③ BG 灰 + Screen       把纯黑抬到深灰 BG（默认 0.12 ≈ #1f1f1f），不刺眼也不死黑
    ④ FG 灰 + Multiply     只有 --fg < 1 时才做：把纯白压到米白
    --invert-only 只做 ①。

用法：
    python3 tools/pdf_dark.py <in.pdf> [<out.pdf>]        默认输出到同目录 problem_dark.pdf
    python3 tools/pdf_dark.py --all                        题库里每个 problem.pdf 旁边生成 problem_dark.pdf（已有的会重做）
    python3 tools/pdf_dark.py --inplace <in.pdf>           原地覆盖
    python3 tools/pdf_dark.py --bg 0.12 --boost 0.35 --fg 1 <in.pdf>   调背景亮度 / 文字提亮 / 文字压暗
依赖：pikepdf（pip install pikepdf）
"""
from __future__ import annotations
import sys
from pathlib import Path

import pikepdf


BG_DEFAULT, BOOST_DEFAULT, FG_DEFAULT = 0.12, 0.35, 1.0


def darken(src: Path, dst: Path, bg: float = BG_DEFAULT, boost: float = BOOST_DEFAULT, fg: float = FG_DEFAULT,
           invert_only: bool = False) -> None:
    pdf = pikepdf.open(src)
    steps = [("/GSInv", "/Difference", 1.0)]
    if not invert_only:
        if boost > 0:
            steps.append(("/GSBoost", "/ColorDodge", boost))
        steps.append(("/GSBg", "/Screen", bg))
        if fg < 1:
            steps.append(("/GSFg", "/Multiply", fg))
    for page in pdf.pages:
        page = pikepdf.Page(page)
        res = page.obj.get("/Resources")
        if res is None:
            res = page.obj.Resources = pikepdf.Dictionary()
        eg = res.get("/ExtGState")
        if eg is None:
            eg = res.ExtGState = pikepdf.Dictionary()
        for name, bm, _ in steps:
            eg[name] = pdf.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name("/ExtGState"), BM=pikepdf.Name(bm), CA=1, ca=1))
        x0, y0, x1, y1 = (float(v) for v in page.mediabox)
        rect = f"{x0} {y0} {x1 - x0} {y1 - y0} re f"
        overlay = "".join(f"q {name} gs {gray:.3f} g {rect} Q\n" for name, _, gray in steps).encode()
        # 先铺一层实打实的白底：没画过东西的地方 backdrop 是"透明"而不是白，Difference 对透明没作用，
        # 结果就是整页还是白的（Chrome 导出的 PDF 有的会画白底，有的不会，LC-0187 就是不画的那种）。
        # 再用 q…Q 把原内容包起来，避免原内容末尾残留的图形状态影响我们的矩形。
        base = f"q 1 g {rect} Q\nq\n".encode()
        page.contents_add(pikepdf.Stream(pdf, base), prepend=True)
        page.contents_add(pikepdf.Stream(pdf, b"\nQ\n" + overlay))
    pdf.save(dst)


def darken_all(root: Path, **kw) -> None:
    import os
    ok = fail = 0
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if not d.startswith(("$$", ".", "__pycache__")) and d not in ("tools", "New", "Today")]
        if "problem.pdf" in fns and "metadata.json" in fns:
            src = Path(dp) / "problem.pdf"
            try:
                darken(src, src.with_name("problem_dark.pdf"), **kw); ok += 1
            except Exception as e:  # noqa: BLE001
                fail += 1; print(f"  ✗ {os.path.relpath(dp, root)}: {e}")
    print(f"🌙 problem_dark.pdf：成功 {ok}，失败 {fail}")


def main(argv: list[str]) -> None:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip()); return
    if "--all" in argv:
        darken_all(Path(__file__).resolve().parent.parent); return
    inplace = "--inplace" in argv
    invert_only = "--invert-only" in argv
    bg, boost, fg = BG_DEFAULT, BOOST_DEFAULT, FG_DEFAULT
    args = []
    it = iter(argv)
    for a in it:
        if a in ("--inplace", "--invert-only"):
            continue
        if a == "--bg":
            bg = float(next(it)); continue
        if a == "--boost":
            boost = float(next(it)); continue
        if a == "--fg":
            fg = float(next(it)); continue
        args.append(a)
    src = Path(args[0])
    if inplace:
        tmp = src.with_suffix(".dark.tmp.pdf")
        darken(src, tmp, bg, boost, fg, invert_only); tmp.replace(src); print(f"✅ 已原地变暗：{src}")
        return
    dst = Path(args[1]) if len(args) > 1 else src.with_name("problem_dark.pdf")
    darken(src, dst, bg, boost, fg, invert_only)
    print(f"✅ {dst}")


if __name__ == "__main__":
    main(sys.argv[1:])
