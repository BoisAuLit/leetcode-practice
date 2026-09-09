---
name: intake
description: 把 New/ 里的新题（solution.py + 可选笔记）入库到题库对应的子分类文件夹。用户说"入库"、"intake"、"把 New 里的题归档"时使用。人机协作：脚本负责校验和搬运，Claude 负责判断子分类并和用户确认。
---

# 新题入库（New/ → 题库）

仓库根目录：`/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice`（所有命令在这里执行）。

## 约定

- 用户做新题时只在 `New/` 里放一个 `solution.py`，**第一行**是链接注释：
  `# https://leetcode.com/problems/<slug>/...` 或 `# https://neetcode.io/problems/<slug>/question?list=neetcode150`
- `New/` 里的其他文件（手写笔记图片、PDF、md）会原样进入该题的 `assets/`。
- 目标结构：`<大类>/<子分类>/LC-0187 - Title/`（NeetCode 题为 `NC - Title/`），内含 `solution.py`、`metadata.json`、`problem.pdf`、可选 `assets/`。
- 子分类命名风格：`kebab-case (中文)`，例如 `monotonic-stack (单调栈)`；归不进任何子分类就用该大类下的 `general/`（不存在就创建）。

## 步骤

1. **校验并解析**（不改任何东西）：
   ```bash
   python3 tools/intake.py --dry-run
   ```
   任何前提不满足（没有 solution.py、第一行不是链接、链接不认识）脚本会直接报错退出 —— 把错误原样告诉用户，不要替他猜测或修改 solution.py。
   成功时会打印：题目来源（LC/NC）、编号、官方标题、难度、两个链接，以及**所有大类及其现有子分类**。

2. **决定子分类**（这一步是 Claude 的判断，不要跳过确认）：
   - 读一遍 `solution.py`，结合题目标题判断算法归属（例如 Two Sum → `01-arrays-hashing (数组、哈希表)/hash-map (哈希表)`）。
   - 优先复用 dry-run 列出来的**现有**子分类；确实没有合适的才建议新建（给出 kebab-case (中文) 的名字）；都不合适就用 `general`。
   - NeetCode 150 的 section 与大类的对应关系：Arrays & Hashing→01，Two Pointers→02，Sliding Window→03，Stack→04，Binary Search→05，Linked List→06，Trees→07，Tries→08，Heap→09，Backtracking→10，Graphs / Advanced Graphs→11，1-D / 2-D DP→12，Greedy→13，Intervals→14，Bit Manipulation→16，Math & Geometry→15。
   - 用 AskUserQuestion 给出**一个推荐目标 + 最多两个备选**，让用户确认。同时顺便问一句"信号→模式"一句话（可以留空以后再补）。

3. **执行入库**：
   ```bash
   python3 tools/intake.py --target "<大类>/<子分类>" --signal "<信号> → <模式>" [--sticking "<卡点>"] [--guard "<输入 -> 期望>"]
   ```
   如需新建子分类，先 `mkdir` 再执行。脚本会：建文件夹、写 `solution.py`（去掉第一行）、写 `metadata.json`、抓取 `problem.pdf`（调用 tuto_etsy 的 puppeteer 脚本，需要 Chrome Canary 已在 9222 端口运行）、把附带文件搬进 `assets/`、清空 `New/`。

4. **汇报**：把脚本最后打印的目标路径原样告诉用户（"入库到了哪里"），并提醒复习命令：
   `python3 tools/review_due.py done "<题目文件夹名>" <g|y|r> [--note "卡点"]`

## 疑难笔记怎么入库

- 做题当天的笔记：和 `solution.py` 一起放进 `New/`，入库时自动进 `assets/`。
- 事后补的笔记：直接放进该题文件夹的 `assets/`（没有就建一个），文件名里别用 emoji。
- 卡点（sticking point）：入库时用 `--sticking`，或复习时用 `review_due.py done ... --note "..."` 追加到 `practice[]`。
- 守卫反例（guard）：真实踩过的坑的最小反例 `输入 -> 期望`，用 `--guard` 或 `review_due.py init "<题>" "<信号→模式>" --guard "..."` 写入 `metadata.json`。

## 不要做的事

- 不要在 `New/` 缺文件或链接格式不对时自行"修复"再入库 —— 报错并让用户处理。
- 不要用 `rm -rf` 处理任何题目文件夹；仓库的 `.gitignore` 忽略了 PDF 和图片，git 不能恢复它们。
- 不要手改 `metadata.json` 里的 `practice[]`，那是 `review_due.py done` 的领地。
