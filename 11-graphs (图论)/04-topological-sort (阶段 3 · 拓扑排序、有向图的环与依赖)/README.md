# 04-topological-sort (阶段 3 · 拓扑排序、有向图的环与依赖)

**目标**：Kahn 和三色 DFS 都会，知道什么时候选哪个。

**出关标准**：207、210 盲写；能说出"Kahn 顺带数了多少点，数不够就是有环"。

标记：★ 签名题（每个模板只绑一道，进复习系统时优先盲写）· ○ 核心变体 · △ 扩展。
每道题只问一句：**和签名题比改了哪一行？**

## [kahn (Kahn：按入度做 BFS)](kahn%20%28Kahn%EF%BC%9A%E6%8C%89%E5%85%A5%E5%BA%A6%E5%81%9A%20BFS%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 207 Course Schedule](kahn%20%28Kahn%EF%BC%9A%E6%8C%89%E5%85%A5%E5%BA%A6%E5%81%9A%20BFS%29/LC-0207%20-%20Course%20Schedule%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 课程有先修关系，能否全部修完 | Kahn 签名题：入度为 0 的进队列，出队个数 < n 就有环 |
| ○ | [LC 210 Course Schedule II](kahn%20%28Kahn%EF%BC%9A%E6%8C%89%E5%85%A5%E5%BA%A6%E5%81%9A%20BFS%29/LC-0210%20-%20Course%20Schedule%20II) | 输出一个可行的修课顺序 | 207 把出队顺序记下来 |
| ○ | [LC 1557 Minimum Number of Vertices to Reach All Nodes](kahn%20%28Kahn%EF%BC%9A%E6%8C%89%E5%85%A5%E5%BA%A6%E5%81%9A%20BFS%29/LC-1557%20-%20Minimum%20Number%20of%20Vertices%20to%20Reach%20All%20Nodes) | 最少从哪些点出发能到所有点 | 答案就是入度为 0 的点，练入度直觉 |
| ○ | [LC 269 Alien Dictionary](kahn%20%28Kahn%EF%BC%9A%E6%8C%89%E5%85%A5%E5%BA%A6%E5%81%9A%20BFS%29/LC-0269%20-%20Alien%20Dictionary) | 从排好序的外星单词推出字母顺序（会员） | 难点在相邻单词比较建边，再 Kahn，注意前缀特判 |
| ○ | [LC 2115 Find All Possible Recipes from Given Supplies](kahn%20%28Kahn%EF%BC%9A%E6%8C%89%E5%85%A5%E5%BA%A6%E5%81%9A%20BFS%29/LC-2115%20-%20Find%20All%20Possible%20Recipes%20from%20Given%20Supplies) | 有原料，哪些菜能做出来 | 配方当有向边，Kahn 从原料出发 |
| △ | [LC 444 Sequence Reconstruction](kahn%20%28Kahn%EF%BC%9A%E6%8C%89%E5%85%A5%E5%BA%A6%E5%81%9A%20BFS%29/LC-0444%20-%20Sequence%20Reconstruction) | 给定子序列能否唯一确定原序列（会员） | Kahn 时队列里任何时刻都只有一个点 |

## [three-color-dfs (三色 DFS：遇到灰色点 = 有环)](three-color-dfs%20%28%E4%B8%89%E8%89%B2%20DFS%EF%BC%9A%E9%81%87%E5%88%B0%E7%81%B0%E8%89%B2%E7%82%B9%20%3D%20%E6%9C%89%E7%8E%AF%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 802 Find Eventual Safe States](three-color-dfs%20%28%E4%B8%89%E8%89%B2%20DFS%EF%BC%9A%E9%81%87%E5%88%B0%E7%81%B0%E8%89%B2%E7%82%B9%20%3D%20%E6%9C%89%E7%8E%AF%29/LC-0802%20-%20Find%20Eventual%20Safe%20States%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 哪些点出发永远走不进环 | 三色 DFS 签名题（或把边反向后做 Kahn） |
| ○ | [LC 1059 All Paths from Source Lead to Destination](three-color-dfs%20%28%E4%B8%89%E8%89%B2%20DFS%EF%BC%9A%E9%81%87%E5%88%B0%E7%81%B0%E8%89%B2%E7%82%B9%20%3D%20%E6%9C%89%E7%8E%AF%29/LC-1059%20-%20All%20Paths%20from%20Source%20Lead%20to%20Destination) | 从起点出发的每条路都必须终止在终点（会员） | 三色 DFS 判环 + 终点出度必须为 0 |

## [peel-leaves (剥叶子：无向图上的 Kahn)](peel-leaves%20%28%E5%89%A5%E5%8F%B6%E5%AD%90%EF%BC%9A%E6%97%A0%E5%90%91%E5%9B%BE%E4%B8%8A%E7%9A%84%20Kahn%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ○ | [LC 310 Minimum Height Trees](peel-leaves%20%28%E5%89%A5%E5%8F%B6%E5%AD%90%EF%BC%9A%E6%97%A0%E5%90%91%E5%9B%BE%E4%B8%8A%E7%9A%84%20Kahn%29/LC-0310%20-%20Minimum%20Height%20Trees) | 以哪个点为根树最矮 | 从叶子一层层剥，最后剩的 1–2 个点，"剥叶子"就是无向图上的 Kahn |

## [layered (按层：轮数 = 学期数)](layered%20%28%E6%8C%89%E5%B1%82%EF%BC%9A%E8%BD%AE%E6%95%B0%20%3D%20%E5%AD%A6%E6%9C%9F%E6%95%B0%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ○ | [LC 1136 Parallel Courses](layered%20%28%E6%8C%89%E5%B1%82%EF%BC%9A%E8%BD%AE%E6%95%B0%20%3D%20%E5%AD%A6%E6%9C%9F%E6%95%B0%29/LC-1136%20-%20Parallel%20Courses) | 每学期可修任意多门无依赖的课，最少几学期（会员） | Kahn 按层数轮数 |

## [dag-dp (DAG 上的 DP：拓扑序 + 状态转移)](dag-dp%20%28DAG%20%E4%B8%8A%E7%9A%84%20DP%EF%BC%9A%E6%8B%93%E6%89%91%E5%BA%8F%20%2B%20%E7%8A%B6%E6%80%81%E8%BD%AC%E7%A7%BB%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ○ | [Longest Increasing Path in a Matrix (LC 329)](<dag-dp (DAG 上的 DP：拓扑序 + 状态转移)/LC-0329 - Longest Increasing Path in a Matrix>) | 网格里最长递增路径 | 网格是 DAG，记忆化 DFS 就是 DAG 上的 DP |
| △ | [LC 1462 Course Schedule IV](dag-dp%20%28DAG%20%E4%B8%8A%E7%9A%84%20DP%EF%BC%9A%E6%8B%93%E6%89%91%E5%BA%8F%20%2B%20%E7%8A%B6%E6%80%81%E8%BD%AC%E7%A7%BB%29/LC-1462%20-%20Course%20Schedule%20IV) | 多组查询"a 是不是 b 的先修" | 拓扑序 + 每个点维护祖先集合，或 Floyd 传递闭包 |
| △ | [LC 2050 Parallel Courses III](dag-dp%20%28DAG%20%E4%B8%8A%E7%9A%84%20DP%EF%BC%9A%E6%8B%93%E6%89%91%E5%BA%8F%20%2B%20%E7%8A%B6%E6%80%81%E8%BD%AC%E7%A7%BB%29/LC-2050%20-%20Parallel%20Courses%20III) | 课程有时长，最少多少时间修完 | 拓扑序 + DP 求最长路 |
| △ | [LC 1857 Largest Color Value in a Directed Graph](dag-dp%20%28DAG%20%E4%B8%8A%E7%9A%84%20DP%EF%BC%9A%E6%8B%93%E6%89%91%E5%BA%8F%20%2B%20%E7%8A%B6%E6%80%81%E8%BD%AC%E7%A7%BB%29/LC-1857%20-%20Largest%20Color%20Value%20in%20a%20Directed%20Graph) | 有向图路径上同色点最多几个，有环返回 −1 | Kahn 同时做 DP |
| △ | [LC 1203 Sort Items by Groups Respecting Dependencies](dag-dp%20%28DAG%20%E4%B8%8A%E7%9A%84%20DP%EF%BC%9A%E6%8B%93%E6%89%91%E5%BA%8F%20%2B%20%E7%8A%B6%E6%80%81%E8%BD%AC%E7%A7%BB%29/LC-1203%20-%20Sort%20Items%20by%20Groups%20Respecting%20Dependencies) | 两层依赖（组之间、组内） | 做两次拓扑排序 |

---

每题文件夹：`solution.py`（所有解法 + 复杂度 + ⭐ 最优）、`problem.pdf` / `problem_dark.pdf`、`metadata.json`（复习记录）。
模板在 [00-foundations/templates (模板)](../00-foundations%20%28%E5%9B%BE%E8%AE%BA%E5%9F%BA%E7%A1%80%E3%80%81%E5%9B%BE%E8%AE%BA%E6%89%8B%E5%86%8C%29/templates%20%28%E6%A8%A1%E6%9D%BF%29)，总表在 [../README.md](../README.md)。
