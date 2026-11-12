# 01-graph-modeling (阶段 0 · 建图、隐式图、状态图)

**目标**：看到任何输入都能说出"点是什么、边是什么"，不用真的建图也能遍历。

**出关标准**：能把 752 的"密码状态"和 127 的"单词"解释成图上的点。

标记：★ 签名题（每个模板只绑一道，进复习系统时优先盲写）· ○ 核心变体 · △ 扩展。
每道题只问一句：**和签名题比改了哪一行？**

## [degree (度：入度、出度)](degree%20%28%E5%BA%A6%EF%BC%9A%E5%85%A5%E5%BA%A6%E3%80%81%E5%87%BA%E5%BA%A6%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ○ | [LC 997 Find the Town Judge](degree%20%28%E5%BA%A6%EF%BC%9A%E5%85%A5%E5%BA%A6%E3%80%81%E5%87%BA%E5%BA%A6%29/LC-0997%20-%20Find%20the%20Town%20Judge) | 谁被所有人信任且不信任任何人 | 入度 n−1、出度 0。热身，练"度"的概念 |
| ○ | [LC 277 Find the Celebrity](degree%20%28%E5%BA%A6%EF%BC%9A%E5%85%A5%E5%BA%A6%E3%80%81%E5%87%BA%E5%BA%A6%29/LC-0277%20-%20Find%20the%20Celebrity) | 谁被所有人认识且不认识任何人（只能调 knows API） | 和 997 同一个"度"的概念，但不能建图：两遍淘汰，O(n) 次调用 |

## [adjacency-list (显式建图：边列表 → 邻接表)](adjacency-list%20%28%E6%98%BE%E5%BC%8F%E5%BB%BA%E5%9B%BE%EF%BC%9A%E8%BE%B9%E5%88%97%E8%A1%A8%20%E2%86%92%20%E9%82%BB%E6%8E%A5%E8%A1%A8%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 1971 Find if Path Exists in Graph](adjacency-list%20%28%E6%98%BE%E5%BC%8F%E5%BB%BA%E5%9B%BE%EF%BC%9A%E8%BE%B9%E5%88%97%E8%A1%A8%20%E2%86%92%20%E9%82%BB%E6%8E%A5%E8%A1%A8%29/LC-1971%20-%20Find%20if%20Path%20Exists%20in%20Graph%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 边列表建邻接表，u 能否到 v | 建图 + DFS/BFS 的最裸模板 |
| ○ | [LC 841 Keys and Rooms](adjacency-list%20%28%E6%98%BE%E5%BC%8F%E5%BB%BA%E5%9B%BE%EF%BC%9A%E8%BE%B9%E5%88%97%E8%A1%A8%20%E2%86%92%20%E9%82%BB%E6%8E%A5%E8%A1%A8%29/LC-0841%20-%20Keys%20and%20Rooms) | 从 0 号房间出发能否进所有房间 | 有向图可达性，和 1971 一样只是方向性 |
| ○ | [LC 797 All Paths From Source to Target](adjacency-list%20%28%E6%98%BE%E5%BC%8F%E5%BB%BA%E5%9B%BE%EF%BC%9A%E8%BE%B9%E5%88%97%E8%A1%A8%20%E2%86%92%20%E9%82%BB%E6%8E%A5%E8%A1%A8%29/LC-0797%20-%20All%20Paths%20From%20Source%20to%20Target) | 枚举 DAG 上从 0 到 n−1 的所有路径 | DFS + 回溯，path 进出 |
| ★ | [LC 133 Clone Graph](adjacency-list%20%28%E6%98%BE%E5%BC%8F%E5%BB%BA%E5%9B%BE%EF%BC%9A%E8%BE%B9%E5%88%97%E8%A1%A8%20%E2%86%92%20%E9%82%BB%E6%8E%A5%E8%A1%A8%29/LC-0133%20-%20Clone%20Graph%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 深拷贝一张图 | 遍历 + 哈希表"旧点 → 新点"，面试高频 |
| ○ | [LC 1466 Reorder Routes to Make All Paths Lead to the City Zero](adjacency-list%20%28%E6%98%BE%E5%BC%8F%E5%BB%BA%E5%9B%BE%EF%BC%9A%E8%BE%B9%E5%88%97%E8%A1%A8%20%E2%86%92%20%E9%82%BB%E6%8E%A5%E8%A1%A8%29/LC-1466%20-%20Reorder%20Routes%20to%20Make%20All%20Paths%20Lead%20to%20the%20City%20Zero) | 树上有向边，最少反转几条让所有城市能到 0 | 建图时给边打"正向/反向"标记，从 0 出发 DFS 数反向边 |

## [state-graph-bfs (状态图 BFS：一个状态就是一个点)](state-graph-bfs%20%28%E7%8A%B6%E6%80%81%E5%9B%BE%20BFS%EF%BC%9A%E4%B8%80%E4%B8%AA%E7%8A%B6%E6%80%81%E5%B0%B1%E6%98%AF%E4%B8%80%E4%B8%AA%E7%82%B9%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 752 Open the Lock](state-graph-bfs%20%28%E7%8A%B6%E6%80%81%E5%9B%BE%20BFS%EF%BC%9A%E4%B8%80%E4%B8%AA%E7%8A%B6%E6%80%81%E5%B0%B1%E6%98%AF%E4%B8%80%E4%B8%AA%E7%82%B9%29/LC-0752%20-%20Open%20the%20Lock%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 四位转盘锁最少转几次到目标，有死锁状态 | 状态图 BFS 签名题：点 = 一个四位串，边 = 拨一位 |
| ○ | [LC 127 Word Ladder](state-graph-bfs%20%28%E7%8A%B6%E6%80%81%E5%9B%BE%20BFS%EF%BC%9A%E4%B8%80%E4%B8%AA%E7%8A%B6%E6%80%81%E5%B0%B1%E6%98%AF%E4%B8%80%E4%B8%AA%E7%82%B9%29/LC-0127%20-%20Word%20Ladder) | 单词每次改一个字母，最少几步变成目标 | 隐式图 BFS，用通配符 h*t 建邻居；可升级成双向 BFS |
| ○ | [LC 433 Minimum Genetic Mutation](state-graph-bfs%20%28%E7%8A%B6%E6%80%81%E5%9B%BE%20BFS%EF%BC%9A%E4%B8%80%E4%B8%AA%E7%8A%B6%E6%80%81%E5%B0%B1%E6%98%AF%E4%B8%80%E4%B8%AA%E7%82%B9%29/LC-0433%20-%20Minimum%20Genetic%20Mutation) | 基因串每次改一个字符 | 127 的小号版 |
| △ | [LC 773 Sliding Puzzle](state-graph-bfs%20%28%E7%8A%B6%E6%80%81%E5%9B%BE%20BFS%EF%BC%9A%E4%B8%80%E4%B8%AA%E7%8A%B6%E6%80%81%E5%B0%B1%E6%98%AF%E4%B8%80%E4%B8%AA%E7%82%B9%29/LC-0773%20-%20Sliding%20Puzzle) | 2×3 滑块拼图最少几步复原 | 状态 = 整个棋盘序列化成字符串，BFS |
| △ | [LC 909 Snakes and Ladders](state-graph-bfs%20%28%E7%8A%B6%E6%80%81%E5%9B%BE%20BFS%EF%BC%9A%E4%B8%80%E4%B8%AA%E7%8A%B6%E6%80%81%E5%B0%B1%E6%98%AF%E4%B8%80%E4%B8%AA%E7%82%B9%29/LC-0909%20-%20Snakes%20and%20Ladders) | 蛇梯棋最少掷几次 | 一维编号和二维坐标互转，BFS |

---

每题文件夹：`solution.py`（所有解法 + 复杂度 + ⭐ 最优）、`problem.pdf` / `problem_dark.pdf`、`metadata.json`（复习记录）。
模板在 [00-foundations/templates (模板)](../00-foundations%20%28%E5%9B%BE%E8%AE%BA%E5%9F%BA%E7%A1%80%E3%80%81%E5%9B%BE%E8%AE%BA%E6%89%8B%E5%86%8C%29/templates%20%28%E6%A8%A1%E6%9D%BF%29)，总表在 [../README.md](../README.md)。
