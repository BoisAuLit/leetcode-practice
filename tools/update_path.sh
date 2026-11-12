#!/bin/zsh
# update_path.sh — 把题库里每道题 metadata.json 的 path 字段刷成它当前真实的相对路径。
#
# 什么时候用：手动挪动/重命名过题目文件夹之后（拖进 cluster、换子分类、改文件夹名…）。
# 已经对得上的 metadata.json 一个字节都不碰（mtime 也不变），只改真正需要改的。
# path 永远放在 id 后面；文件里没有 path 字段就补一个。
#
# 用法：  update_path            （~/.zshrc 里的 alias）
#        tools/update_path.sh [-n|--dry-run]    只看要改哪些，不真改
set -e
ROOT="${0:A:h:h}"          # 脚本在 tools/ 下，上一级就是仓库根目录
exec python3 - "$ROOT" "$@" <<'PY'
import json, os, re, sys
from collections import OrderedDict

root = sys.argv[1]
dry = any(a in ("-n", "--dry-run") for a in sys.argv[2:])
PROBLEM_DIR_RE = re.compile(r"^(?:\d{1,2} *- *)?(LC-\d{4}|NC) - ")   # 可选的数字优先级前缀，两种写法都认：01-LC-0876 - Title / 01 - LC-0743 - Title
SKIP_DIRS = {"tools", "New", "Today", "__pycache__", ".git", ".vscode"}

checked = updated = added = broken = 0
for dp, dns, fns in os.walk(root):
    dns[:] = [d for d in dns if d not in SKIP_DIRS and not d.startswith(("$$", "."))]
    if "metadata.json" not in fns or not PROBLEM_DIR_RE.match(os.path.basename(dp)):
        continue
    checked += 1
    f = os.path.join(dp, "metadata.json")
    rel = os.path.relpath(dp, root)
    try:
        meta = json.load(open(f, encoding="utf-8"), object_pairs_hook=OrderedDict)
    except Exception as e:                                   # noqa: BLE001
        broken += 1
        print(f"  ⚠️  读不了，跳过：{rel}  ({e})")
        continue
    old = meta.get("path")
    if old == rel:
        continue                                             # 已经对了 → 完全不碰这个文件
    # 重建，保证 path 紧跟在 id 后面
    out = OrderedDict()
    for k, v in meta.items():
        if k == "path":
            continue
        out[k] = v
        if k == "id":
            out["path"] = rel
    if "path" not in out:                                    # 没有 id 的兜底：放第二位
        out = OrderedDict([(list(out)[0], out[list(out)[0]]), ("path", rel)]
                          + [(k, v) for k, v in list(out.items())[1:]])
    updated += 1
    if old is None:
        added += 1
        print(f"  ➕ {rel}  （原来没有 path）")
    else:
        print(f"  🔧 {old}\n     → {rel}")
    if not dry:
        with open(f, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=2)
            fh.write("\n")

verb = "需要更新" if dry else "已更新"
print(f"\n✅ 检查 {checked} 道题：{verb} {updated} 个 path"
      + (f"（其中新增 {added} 个）" if added else "")
      + f"，{checked - updated - broken} 个本来就是对的，没有改动"
      + (f"，{broken} 个 metadata.json 读不了" if broken else "")
      + ("\n（--dry-run：什么都没写）" if dry and updated else ""))
PY
