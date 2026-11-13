---
name: intake
description: 把 New/ 里的新题（solution.py + 可选笔记）入库到题库对应的子分类文件夹。用户说"入库"、"intake"、"把 New 里的题归档"时使用。人机协作：脚本负责校验和搬运，Claude 负责判断子分类并和用户确认。
---

# 入库（New/ → 题库；或补全已归类的题）

仓库根目录：`/Users/bohaoli/Desktop/tuto/tuto_leetcode/leetcode-practice`（所有命令在这里执行）。

## 约定

- 用户做新题时只在 `New/` 里放一个 `solution.py`，**第一行**是链接注释（可选再放一个 `note.md`，会成为该题的 `note.md`）：
  `# https://leetcode.com/problems/<slug>/...` 或 `# https://neetcode.io/problems/<slug>/question?list=neetcode150`
- `New/` 里的其他文件（手写笔记图片、PDF…）会进入该题文件夹**根目录**，文件名加 `asset-` 前缀（不再有 `assets/` 子文件夹）。
- 目标结构：`<大类>/<子分类>/LC-0187 - Title/`（NeetCode 题为 `NC - Title/`），内含 `solution.py`、`metadata.json`、`problem.pdf`、`problem_dark.pdf`、可选 `note.md`（文字笔记）、可选 `asset-*`（图片等附件，直接摊在这一层）。
- `metadata.json` 只有 `id` / `path` / `difficulty` / `link` / `practice`。**标题、信号→模式都不记在 metadata 里**：用户想记信号就自己挂在文件夹名后面（`LC-0187 - Title - <信号/备注>`），脚本只认 `LC-xxxx - ` / `NC - ` 前缀，后面随便写。
- 子分类命名风格：`kebab-case (中文)`，例如 `monotonic-stack (单调栈)`；归不进任何子分类就用该大类下的 `general/`（不存在就创建）。

## 两种模式

- **`/intake`（没有参数）** → 处理 `New/` 里的新题，走下面的「步骤」。
- **`/intake "<绝对路径>"`（有参数）** → 这题用户已经自己归好类了，只是缺文件，走「模式二」。参数是某道题的 `solution.py` 绝对路径（路径里有空格，一定带引号），也可以是题目文件夹、cluster 文件夹或子分类文件夹。

## 模式二：补全已归类的题（有参数时）

```bash
python3 tools/intake.py "<用户给的路径>"            # 可以一次给多个路径；--no-pdf 跳过抓题面；--force 覆盖已有文件
```

脚本会：读 `solution.py` 第一行的链接（读完从代码里删掉；没有链接就用文件夹名里的 `LC-编号` / `NC 标题` 反查）→ 写 `metadata.json`（含 `path`）→ 抓 `problem.pdf` → 生成 `problem_dark.pdf`。**文件夹原地不动**（位置是用户自己归的类，不要移动、不要改名，包括单调题也不强制搬走），已存在的文件默认跳过。传 cluster / 子分类文件夹时，里面每个带 `solution.py` 的子文件夹都会被补全。

这一步**不需要问用户**分类，因为分类已经是用户选的。做完汇报：补了哪几道题、每道补了哪些文件。如果脚本报错（文件夹名没有 `LC-1234 - ` / `NC - ` 前缀、第一行不是链接又反查不到），把错误原样告诉用户，不要自己改名或猜链接。

## 步骤（模式一：`New/` 里的新题）

1. **校验并解析**（不改任何东西）：
   ```bash
   python3 tools/intake.py --dry-run
   ```
   任何前提不满足（没有 solution.py、第一行不是链接、链接不认识）脚本会直接报错退出 —— 把错误原样告诉用户，不要替他猜测或修改 solution.py。
   成功时会打印：题目来源（LC/NC）、编号、官方标题、难度、两个链接，以及**所有大类及其现有子分类**。

1.5 **查重（旧题分支）**：dry-run 成功后，先在题库里找同名题目文件夹（`find . -maxdepth 5 -iname "* - <官方标题>*"`（图论是 `<大类>/<阶段>/<模板>/<题>` 四级，所以要 `-maxdepth 5`；文件夹名可能带 ` - ★ 签名题` 之类的后缀，所以末尾要 `*`），LC-xxxx 和 NC 前缀都算）。找到了就是**旧题**，不走 intake.py，直接按下面处理，**不用问用户**（子分类沿用旧文件夹，复习结果默认 🔴）：
   - `solution.py`：用 `New/solution.py` 去掉第一行后**整体覆盖**旧文件夹的 `solution.py`，旧解法不保留。
   - 笔记：用户在 `/intake` 参数里给的笔记原样**追加**进 `<旧题>/note.md`（和 solution.py 同级；没有就建，标题 `# <title> 笔记`；已有内容不要动，末尾加一节 `### 📝 <日期> - 入库笔记`）；`New/` 里的其他附带文件搬进题目文件夹根目录并加 `asset-` 前缀（`New/note.md` 例外：并进 `<旧题>/note.md`）。
   - 复习记录：`python3 tools/review_due.py done "<旧题文件夹名>" r --note "<用户笔记或卡点>"`。**所有刚做过的题一律记 🔴**，不问颜色；用户在参数里明确说了颜色才用那个颜色。
   - 最后 `rm New/solution.py`（以及已搬走的附带文件），确认 `New/` 为空。
   - 汇报：旧题路径、覆盖了什么、下次复习日期。

2. **决定子分类**（这一步是 Claude 的判断，不要跳过确认）：
   - 读一遍 `solution.py`，结合题目标题判断算法归属（例如 Two Sum → `01-arrays-hashing (数组、哈希表)/hash-map (哈希表)`）。
   - 优先复用 dry-run 列出来的**现有**子分类；确实没有合适的才建议新建（给出 kebab-case (中文) 的名字）；都不合适就用 `general`。
   - **单调栈 / 单调队列铁律**：题目、解法或笔记里只要和 monotonic stack / monotonic queue / 单调栈 / 单调队列沾边（Next Greater Element、Daily Temperatures、Sliding Window Maximum、Largest Rectangle in Histogram、Trapping Rain Water、Remove K Digits 这一类），**不问用户，直接归到 `18-monotonic-fuck-you (单调栈、单调队列)`**：单调栈 → `monotonic-stack (单调栈)`，单调队列 → `monotonic-queue (单调队列)`，拿不准 → `general`。intake.py 自己也会检测并强制改 target，所以就算选错了也会被纠正。用户要专门集中练这一类。
   - **图论两级分类**：`11-graphs (图论)` 下面是 `<阶段>/<模板>` 两级（阶段 0–6，总表在 `11-graphs (图论)/README.md`，每个阶段文件夹里还有自己的 `README.md` 列出模板和已有题目）。图论题的 `--target` 必须给到模板那一级，例如 `11-graphs (图论)/02-dfs-bfs (阶段 1 · DFS、BFS：静态无权的连通性与步数)/multi-source-bfs (多源 BFS：所有起点一起入队)`；用 README 里的"五个问题"决定阶段：边有权 → 阶段 4/5，图会变（边一条条来）→ 阶段 2，有方向且问顺序 → 阶段 3，二分图/桥/欧拉 → 阶段 6，否则 → 阶段 0/1。手册点名的 ★ 签名题入库后把文件夹名末尾加 ` - ★ 签名题`（`mv` 改名即可，`update_path` 会修 path），其他题不要加。
   - NeetCode 150 的 section 与大类的对应关系：Arrays & Hashing→01，Two Pointers→02，Sliding Window→03，Stack→04，Binary Search→05，Linked List→06，Trees→07，Tries→08，Heap→09，Backtracking→10，Graphs / Advanced Graphs→11，1-D / 2-D DP→12，Greedy→13，Intervals→14，Bit Manipulation→16，Math & Geometry→15。
   - 用 AskUserQuestion 给出**一个推荐目标 + 最多两个备选**，让用户确认。不要问"信号→模式"：它不进 metadata，用户想记就自己写进文件夹名。

3. **执行入库**：
   ```bash
   python3 tools/intake.py --target "<大类>/<子分类>"
   ```
   如需新建子分类，先 `mkdir` 再执行。脚本会：建文件夹、写 `solution.py`（去掉第一行）、写 `metadata.json`、抓取 `problem.pdf`（调用 tuto_etsy 的 puppeteer 脚本，需要 Chrome Canary 已在 9222 端口运行）、把附带文件搬进 `assets/`、清空 `New/`。

4. **汇报**：把脚本最后打印的目标路径原样告诉用户（"入库到了哪里"），并提醒复习命令：
   `python3 tools/review_due.py done "<题目文件夹名>" <g|y|r> [--note "卡点"]`

## 疑难笔记怎么入库

- 一道题的所有文字笔记都在该题文件夹的 `note.md`（和 solution.py 同级）：intake 的笔记、`done --note` 的卡点、`solution_retry.py` 里带注释的 class（`### 📝 日期 - retry N`，finish 时自动存）。新题入库时不需要有 note.md，第一条笔记产生时才建。
- 图片 / PDF / 手写扫描等非文字附件：和 `solution.py` 一起放进 `New/`，入库时自动搬到题目文件夹根目录并加 `asset-` 前缀；事后补的直接丢进该题文件夹并自己加 `asset-` 前缀，文件名里别用 emoji。`New/note.md` 会并进该题的 `note.md`。
- 卡点（sticking point）：复习时用 `review_due.py done ... --note "..."` 追加到 `practice[]`；入库当天的卡点写进 `New/note.md` 一起入库。
- 守卫反例（guard）：只记在 `MISTAKES.md` 对应错误模式的 **守卫反例** 下（手动维护），不进 `metadata.json`。

## 不要做的事

- 不要在 `New/` 缺文件或链接格式不对时自行"修复"再入库 —— 报错并让用户处理。
- 不要用 `rm -rf` 处理任何题目文件夹；仓库的 `.gitignore` 忽略了 PDF 和图片，git 不能恢复它们。
- 不要手改 `metadata.json` 里的 `practice[]`，那是 `review_due.py done` 的领地。
- 旧题不要再新建 `NC - Title/` 文件夹，题库里一道题只能有一个文件夹，否则复习队列会出现重复。
