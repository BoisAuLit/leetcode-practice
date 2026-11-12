# 11-graphs 重构审计报告

## 原始文件保留
迁移前 524 个文件（不含 `.DS_Store`）。SHA-256 逐个比对：

- **515 个逐字节未变**
- **9 个有意变更**：
  - **6 个主位置的 solution.py**：各自并入了「同题另一算法」的实现作为 `Solution_*_Alt`
    （LC-0787、LC-1368、LC-2290、LC-1334、LC-2976、LC-1631）。
    原有代码一行没动，只是在文件末尾追加。
  - **3 个 README.md**：根 README（追加本次说明）、`05-shortest-path/README.md`、
    `04-topological-sort/README.md`（修死链）。

**没有任何 solution.py 被覆盖，没有任何文件被删除。**

## 六组「同题多算法」的处理（本次重点）

六个重复 LC 编号（0787、1334、1368、1631、2290、2976）**各有两份不同算法的实现**。

**判断依据是文件实际内容，不是 LC 编号** —— 这六组涉及
Bellman-Ford、Dijkstra、0-1 BFS、Floyd-Warshall、瓶颈路径五种不同算法，
**绝不能当作重复文件删除**。

处理方式（三步，零删除）：
1. **指定主学习位置**（Primary），依据 instructions.md 第四、五节的明确表述。
2. 把非主位置的实现**并入主位置的 solution.py**，类名加 `_Alt` 后缀，
   只搬 import 和 class（不搬原文件底部的驱动代码，以免干扰测试）。
3. 非主位置的**目录改名为「变体 · …」**。这个前缀不再匹配
   `PROBLEM_DIR_RE = ^(?:\d{1,2} *- *)?(LC-\d{4}|NC) - `，
   所以 `review_due.py` 的复习队列里一道题只会出现一次。
   **目录里的 solution.py / problem.pdf / metadata.json / 笔记全部原地保留。**

| LC | Primary | Alternative（已改名） |
|---|---|---|
| 0787 | bellman-ford（★ 签名题） | `dijkstra/05 - …/变体 · 01 - LC-0787 …` |
| 1368 | zero-one-bfs | `dijkstra/04 - …/变体 · 02 - LC-1368 …` |
| 2290 | zero-one-bfs | `dijkstra/04 - …/变体 · 01 - LC-2290 …` |
| 1334 | dijkstra/01/02 | `floyd/变体 · LC-1334 … ★ 签名题` |
| 2976 | dijkstra/01/04 | `floyd/变体 · LC-2976 …` |
| 1631 | dijkstra/02/01 | `bottleneck-path/变体 · LC-1631 …` |

**已知取舍**：变体目录不再被 `tools/update_path.sh` 维护（它只认题目前缀），
所以那几个 `metadata.json` 的 `path` 字段会停在改名前的值。
变体目录不参与复习调度，这个不准确不影响任何工具。

**执行过程中的一次返工**（如实记录）：第一次合并时我用正则给搬过来的代码
统一加了 `_Alt` 后缀，但**连它原文件底部的驱动代码一起搬了**，
那些代码引用的是改名前的类名 ⟹ 3 个文件直接跑不起来，
另外 1 个文件的断言还跑在了主位置的类上、报出假错误。
已改为用 `ast` 解析、**只保留 import 和 class 定义**，重做一遍后 117/117 全部通过。

## NC-only 正式化

| 原 NC | 升格为 | practice | 特别保留 |
|---|---|---|---|
| `NC - Longest Increasing Path in Matrix` | `LC-0329 - Longest Increasing Path in a Matrix` | 0 条 | `asset-NC-07 - LC-0329 - Explanation.jpg` 原位未动 |

`metadata.id` 从 `NC-longest-increasing-path-in-matrix` 改为 `LC-0329`，
并补上官方 leetcode 链接。**没有建 `_neetcode/`** —— 仓库现行规则是
「LC / NC 重复时只保留 LeetCode 版」，而这是孤儿 NC，所以是升格而非归档。

## 新增题目（6 道，均含 metadata.json + problem.pdf + problem_dark.pdf）

**第一轮 4 道**：LC-1293、LC-0815、LC-0959、LC-2192
**第二轮自主新增 2 道**：LC-0847、LC-1519

每道都带 2–3 种解法 + 随机对拍：
- LC-1293：600 组，三维 visited 版 vs 最少额度剪枝版 vs 朴素状态 BFS
- LC-0815：800 组，隐式 `stop→routes` vs 显式路线两两建边
- LC-0959：500 组，4 三角形并查集 vs 3× 放大 flood fill
- LC-2192：600 组，Kahn 传播 vs 逐点正向 DFS，并校验输出升序
- LC-0847：400 组，多源位掩码 BFS vs Floyd + 状压 DP
- LC-1519：600 组三方对拍，**额外用 n=20000 的链状树验证迭代 DFS 不爆栈**

## 结构决策：为什么没有改 Level 1 目录名

instructions.md 建议 8 个 Level 1 名字。现有的阶段目录就是这 8 个 Level 1，
只是名字带「阶段 N」。**刻意不改名**，三条理由：

1. instructions.md 自己要求「请优先保留原有阶段式学习逻辑」。
2. 项目技能 **`.claude/skills/intake`** 里把这些路径写死成了入库示例，改名会让技能失效。
3. 04-stack-queue / 06-linked-list / 07-trees 的 README 里已有**十几条**指向这些路径的
   跨专题链接，改名会全部变成死链。

对应关系已在根 README 第一节列出。

## 修复的 13 条死链

本专题原有 13 条失效的相对链接（指向更早一次 dijkstra 重构中已改名的目录）：
`05-shortest-path/README.md` 12 条 + 根 `README.md` 1 条。
连同本次改名产生的新链接一起**全部修复**。

修复过程：先用脚本按「目录 basename / LC 编号」自动匹配修好 16 条，
剩下 5 条是结构性的（指向已不存在的 `dijkstra (Dijkstra 堆版…)`、
`dijkstra-state (…)` 等旧模板目录），手工指向了正确的新位置。
**注意这些链接在源文件里是百分号编码的**，所以必须解码后再匹配。

## 校验结果
- 原始文件：524 个，**515 逐字节一致 + 9 个已逐条说明的有意变更**
- README 相对链接：**201 条，死链 0**
- `solution.py` 运行：**117 / 117 通过**（迁移前 111/111）
- 题目文件夹 117 个，编号连续
- 写入范围：全部在 `11-graphs (图论)/` 之内
- 未执行 `git add` / `commit` / `push`；未使用 `rm -rf`
