# tools/ — 入库、复习调度、错题建档

题库结构（每题一个文件夹）：

```
<大类>/<子分类>/LC-0155 - Min Stack/        ← NeetCode 题为 NC - <标题>/
    solution.py      解法（多解法合并在一个文件里：class Solution_1_xxx, Solution_2_yyy …）
    problem.pdf      题面
    metadata.json    唯一真相：链接、信号→模式、守卫、卡点、首次日期、复习记录 practice[]
    assets/          你自己的笔记（图片 / PDF / md），有才存在
```

## 每天的固定流程（约 15–45 分钟）

```bash
python3 tools/review_due.py shuffle          # ① 选出今天要复习的题（到期优先，不足 3 题从未排期跨分类补足），软链接放进 Today/
# ② 对 Today/ 里的每一题：盖住 solution.py，只看 metadata.json 里的 signal→mode 先口头回答 → 闭卷重写 → 跑守卫反例 → 对照原解
python3 tools/review_due.py done "Min Stack" g --note "卡点一句话"   # ③ 记结果：g=🟢 闭卷流畅  y=🟡 有印象但慢  r=🔴 卡壳
# ④ 出了 bug → MISTAKES.md 归入已有模式（复发 +1）或新建；把守卫反例写进 metadata：review_due.py init "<题>" "<信号→模式>" --guard "..."
git add -A && git commit -m "review $(date +%F)"    # ⑤ 每天一提交
```

## 做新题（入库）

1. 在 `New/` 里写 `solution.py`，第一行是链接注释：`# https://leetcode.com/problems/<slug>/...` 或 `# https://neetcode.io/problems/<slug>/question?list=neetcode150`；手写笔记也丢进 `New/`。
2. 在 Claude Code 里说"入库"（触发 `.claude/skills/intake`），或手动：
   ```bash
   python3 tools/intake.py --dry-run                                   # 校验 + 列出所有子分类
   python3 tools/intake.py --target "<大类>/<子分类>" --signal "信号 → 模式"
   ```
   脚本会建文件夹、写 solution.py / metadata.json、抓 problem.pdf、把笔记搬进 assets/，然后清空 `New/`。

## 全部命令

```bash
python3 tools/review_due.py today [-n 3]        # 只打印今天该复习什么
python3 tools/review_due.py shuffle [-n 3]      # 同上，并重建 Today/ 里的软链接（只清软链接，不碰真实文件）
python3 tools/review_due.py done <子串> g|y|r [--note "卡点"]
python3 tools/review_due.py stats               # 总量、到期/排期/未排期/毕业、按大类进度、最近 🔴
python3 tools/review_due.py list due|unscheduled|scheduled|graduated|all
python3 tools/review_due.py init <子串> "<信号→模式>" [--guard "..."] [--sticking "..."]
python3 tools/intake.py --dry-run
python3 tools/intake.py --target "<大类>/<子分类>" [--signal ...] [--guard ...] [--sticking ...] [--no-pdf]
```

`<子串>` 匹配题目文件夹的相对路径（大小写不敏感），多个命中会列出候选。

## 调度规则

- 间隔阶梯 1 → 3 → 7 → 14 → 30 天；🟢 升一级，🟡 不变，🔴 重置到 1 天；30 天这一级再拿 🟢 = 毕业，不再叫号。
- "下次复习日期"和"是否毕业"不存文件，每次从 `practice[]` 现算 —— 所以永远不会和记录不一致。
- 补足未排期的题时按大类轮转（交错练习），从**已进入循环的题最少**的大类开始，每个大类里先取首次做题最早的。

## 说明

- 只处理带 `metadata.json` 的题目文件夹；`$$-垃圾-可忽略`、`tools/`、`New/`、`Today/`、`__pycache__` 一律忽略。
- `.gitignore` 忽略 PDF / 图片 / `assets/`，**git 恢复不了它们**，删题目文件夹前请三思。
- `tools/legacy/` 是 docstring 复习头时代的旧工具，已不再使用，仅留档。
- 抓题面 PDF 依赖 `tuto_etsy` 项目的 puppeteer 脚本和 9222 端口上已登录的 Chrome Canary。
