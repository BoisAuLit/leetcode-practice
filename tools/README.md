# tools/ — 入库、复习调度、错题建档

题库结构（每题一个文件夹）：

```
<大类>/<子分类>/LC-0155 - Min Stack - O(1) getMin → 双栈/     ← NeetCode 题为 NC - <标题>/；标题后面可以再挂 " - <信号/备注>"，信号→模式就写在文件夹名里
    solution.py      解法（多解法合并在一个文件里：class Solution_1_xxx, Solution_2_yyy …）
    problem.pdf      题面
    problem_dark.pdf 题面夜间版（颜色反转 + 深灰底 + 提亮文字，文字仍可选可搜；intake 自动生成）
    metadata.json    id、path、难度、链接、复习记录 practice[]（标题和信号→模式不在这里，看文件夹名）
    note.md          这道题的全部文字笔记：intake 时的笔记、finish 的评语（### 💬）、solution_retry.py 里带注释的 class（### 📝 retry N）；第一条笔记产生时才建
    asset-*          图片 / PDF 等非文字附件，直接摊在这一层（asset-<原名>），有才存在
```

## 每天的固定流程（约 15–45 分钟）

```bash
shuffle              # ① 从 20 题候选池（到期题 + 从未复习的题）随机抽 5 题，软链接放进 Today/；shuffle 3 改数量
                     #    每题文件夹里生成 solution_retry.py（solution.py 的副本：class 方法体全换成 pass、删掉因此用不到的 import、开头加题目链接，其余原样）
# ② 对 Today/ 里的每一题：盖住 solution.py，只看文件夹名（标题 + 挂在后面的信号）先口头回答 → 在 solution_retry.py 里闭卷重写 → 对照原解
finish 1 g           # ③ 记结果：g=🟢 闭卷流畅  y=🟡 有印象但慢  r=🔴 卡壳；默认 g。会追加 practice[]、把 retry 里带注释的 class 存进 note.md、删 retry、移除软链接
finish 1 r "卡点一句话"   #    带笔记 → 评语追加进 note.md，再用 claude -p 跑 .claude/skills/finish-note，把笔记归入 MISTAKES.md 的错误模式（复发 +1 或新建）
git add -A && git commit -m "review $(date +%F)"    # ④ 每天一提交
```

`shuffle` / `finish` / `review` 定义在 `~/.zshrc`（`review` = `python3 tools/review_due.py`）。悬浮窗小组件（`widget`）上的 Shuffle / 完成按钮调用的就是这两个函数。

## 做新题（入库）

1. 在 `New/` 里写 `solution.py`，第一行是链接注释：`# https://leetcode.com/problems/<slug>/...` 或 `# https://neetcode.io/problems/<slug>/question?list=neetcode150`；手写笔记也丢进 `New/`。
2. 在 Claude Code 里说"入库"（触发 `.claude/skills/intake`），或手动：
   ```bash
   python3 tools/intake.py --dry-run                                   # 校验 + 列出所有子分类
   python3 tools/intake.py --target "<大类>/<子分类>"
   ```
   脚本会建文件夹、写 solution.py / metadata.json、抓 problem.pdf 和 problem_dark.pdf、把附件搬成 `asset-*`，然后清空 `New/`。

## 全部命令

```bash
python3 tools/review_due.py today [-n 3]        # 只打印今天该复习什么（从候选池随机抽 n 题）
python3 tools/review_due.py shuffle [-n 3] [--reset]      # 同上，并重建 Today/ 里的软链接 + 每题生成 solution_retry.py；--reset 才去网站重置旧代码
python3 tools/review_due.py reset [序号]         # 按需：对 Today/ 里的题做网站代码重置（LeetCode / NeetCode，走 tuto_etsy 的 puppeteer 脚本）
python3 tools/review_due.py finish <序号|题目文件夹路径> [g|y|r] [--note "卡点"]   # 按 Today/ 序号（或路径）记结果、删 solution_retry.py、移除软链接
python3 tools/review_due.py done <子串> g|y|r [--note "卡点"]       # 按题目名记结果（不经 Today/）
python3 tools/make_retry.py <题目文件夹或 solution.py>            # 手动生成 solution_retry.py
python3 tools/progress.py                                        # 手动刷新根目录 progress.md（intake / finish / done 会自动刷；shuffle 不刷）
python3 tools/pdf_dark.py --all                                  # 给题库里每个 problem.pdf 生成夜间版 problem_dark.pdf（单个：pdf_dark.py <in.pdf>）
python3 tools/review_due.py stats               # 总量、到期/排期/未排期/毕业、按大类进度、最近 🔴
python3 tools/review_due.py list due|unscheduled|scheduled|graduated|all
python3 tools/intake.py --dry-run
python3 tools/intake.py --target "<大类>/<子分类>" [--no-pdf]
python3 tools/intake.py "<.../LC-3291 - xxx/solution.py>"        # 题已经自己归好类、只缺文件：原地补 metadata.json / problem.pdf / problem_dark.pdf（传 cluster 文件夹则整批补）
```

`<子串>` 匹配题目文件夹的相对路径（大小写不敏感），多个命中会列出候选。

## 单调栈 / 单调队列专区

`18-monotonic-fuck-you (单调栈、单调队列)` 收所有沾边的题（关键词 `monotonic` / `单调栈` / `单调队列`，看文件夹名、solution.py、metadata.json、note.md）。`intake.py` 检测到就强制改 target 到 `.../general`；`review_due.py shuffle` 选题前会把别处的单调题搬到 `.../general`。

## 调度规则

- 间隔阶梯 1 → 3 → 7 → 14 → 30 天；🟢 升一级，🟡 不变，🔴 重置到 1 天；30 天这一级再拿 🟢 = 毕业，不再叫号。
- "下次复习日期"和"是否毕业"不存文件，每次从 `practice[]` 现算 —— 所以永远不会和记录不一致。
- 先凑 20 题候选池，再随机抽 n 题：池 A = **今天到期/逾期**的题按 逾期天数 + 上次🔴ｘ7 / 🟡ｘ3 取前 `POOL_DUE`(10)，池 B = 从未复习过的题按大类轮转随机抽，补足到 20。没到期的题不进池。
- 选定后再随机打乱一次顺序才编号；`shuffle` 先把上一轮的 `solution_retry.py` 和软链接全部清掉，再选题。

## progress.md（进度的唯一来源）

根目录 `progress.md` 由 `tools/progress.py` 生成：总题数按难度、毕业 / 复习中 / 未开始及百分比、总进度（毕业占比）、各级分布、复习记录统计、按大类明细，末尾一个 ```json 块给 macOS 悬浮窗小组件（`tuto_mac_os_widgets/ProgressWidget`，`widget` 启动）读。只在 `intake.py` 和 `review_due.py finish/done` 之后刷新。

## 说明

- `solution_retry.py` 在 `.gitignore` 里，是一次性的草稿，`finish`/`done` 会删掉它。
- 只处理带 `metadata.json` 的题目文件夹；`$$-垃圾-可忽略`、`tools/`、`New/`、`Today/`、`__pycache__` 一律忽略。
- `.gitignore` 忽略 PDF / 图片 / `asset-*`，**git 恢复不了它们**，删题目文件夹前请三思。
- `tools/legacy/` 是 docstring 复习头时代的旧工具，已不再使用，仅留档。
- 抓题面 PDF 和网站代码重置（`review reset` / `shuffle --reset`，脚本 `tuto_etsy/VV-utils/11-reset-code.ts`）都依赖 `tuto_etsy` 项目的 puppeteer 脚本和 9222 端口上已登录的 Chrome Canary（`canary` 启动）；Canary 没开时会跳过并提醒。
