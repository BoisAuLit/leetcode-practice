# 05-shortest-path (阶段 4 · 带权最短路)

**目标**：Dijkstra 堆版闭眼写，知道 relax 那一行怎么改；Bellman-Ford 快照版和 Floyd 能写。

**出关标准**：743、787、1334 盲写；能解释为什么 Dijkstra 不能有负权。

标记：★ 签名题（每个模板只绑一道，进复习系统时优先盲写）· ○ 核心变体 · △ 扩展。
每道题只问一句：**和签名题比改了哪一行？**

## [dijkstra](<dijkstra>)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 743 Network Delay Time](<dijkstra/01 - Dijkstra 标准加法最短路/01 - LC-0743 - Network Delay Time - 教科书>) | 信号从一个点传到所有点要多久 | Dijkstra 堆版签名题，答案是 dist 的最大值 |
| ○ | [LC 1514 Path with Maximum Probability](<dijkstra/02 - Dijkstra 非加法路径代价变体/02 - LC-1514 - Path with Maximum Probability>) | 成功概率最大的路径 | relax 从 d + w 改成 d * p，堆改成大根堆（存负数） |
| ○ | [LC 1976 Number of Ways to Arrive at Destination](<dijkstra/03 - Dijkstra 最短路计数与结果组合/01 - LC-1976 - Number of Ways to Arrive at Destination>) | 最短路有几条 | Dijkstra 加一个 ways 数组，相等时累加，严格更小时覆盖 |
| △ | [LC 505 The Maze II](<dijkstra/04 - Dijkstra 网格建图与特殊边权/01 - LC-0505 - The Maze II>) | 球滚到墙才停，最短滚动距离（会员） | Dijkstra，"邻居"是滚到底的位置 |
| △ | [LC 2642 Design Graph With Shortest Path Calculator](<dijkstra/01 - Dijkstra 标准加法最短路/03 - LC-2642 - Design Graph With Shortest Path Calculator>) | 支持加边和查询最短路 | 每次查询跑一遍 Dijkstra |

## [bottleneck-path (瓶颈路径：relax 改 max 或 min)](bottleneck-path%20%28%E7%93%B6%E9%A2%88%E8%B7%AF%E5%BE%84%EF%BC%9Arelax%20%E6%94%B9%20max%20%E6%88%96%20min%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ○ | [LC 1631 Path With Minimum Effort](<dijkstra/02 - Dijkstra 非加法路径代价变体/01 - LC-1631 - Path With Minimum Effort>) | 路径上相邻高度差的最大值最小 | relax 改成 max(d, w)，瓶颈路径；也可 Kruskal 过程 / 二分 + BFS |
| ○ | [Swim in Rising Water (LC 778)](<dijkstra/02 - Dijkstra 非加法路径代价变体/03 - LC-0778 - Swim in Rising Water>) | 水位涨到多少能游到终点 | 同 1631，阈值在格子上；三种解法都要会说 |
| ○ | [LC 1102 Path With Maximum Minimum Value](bottleneck-path%20%28%E7%93%B6%E9%A2%88%E8%B7%AF%E5%BE%84%EF%BC%9Arelax%20%E6%94%B9%20max%20%E6%88%96%20min%29/LC-1102%20-%20Path%20With%20Maximum%20Minimum%20Value) | 路径最小值最大（会员） | relax 改成 min(d, w) + 大根堆 |

## [dijkstra/05 - Dijkstra 状态扩展与时间约束](<dijkstra/05 - Dijkstra 状态扩展与时间约束>)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| △ | [LC 1928 Minimum Cost to Reach Destination in Time](<dijkstra/05 - Dijkstra 状态扩展与时间约束/01 - LC-1928 - Minimum Cost to Reach Destination in Time>) | 时间限制内最便宜的路 | Dijkstra 的状态变成 (点, 已用时间) |
| △ | [LC 2577 Minimum Time to Visit a Cell In a Grid](<dijkstra/05 - Dijkstra 状态扩展与时间约束/02 - LC-2577 - Minimum Time to Visit a Cell In a Grid>) | 格子有最早可进入时间，可以来回踱步等待 | Dijkstra + 奇偶性处理等待 |
| △ | [LC 2812 Find the Safest Path in a Grid](<dijkstra/02 - Dijkstra 非加法路径代价变体/04 - LC-2812 - Find the Safest Path in a Grid>) | 离小偷最远的一条路 | 先多源 BFS 算每格安全度，再做最大最小值路径 |
| △ | [LC 2203 Minimum Weighted Subgraph With the Required Paths](<dijkstra/03 - Dijkstra 最短路计数与结果组合/03 - LC-2203 - Minimum Weighted Subgraph With the Required Paths>) | 从两个源到一个终点的最小总权 | 正图跑两次 Dijkstra、反图跑一次，枚举汇合点 |

## [zero-one-bfs (0-1 BFS：双端队列，0 放队头 1 放队尾)](zero-one-bfs%20%280-1%20BFS%EF%BC%9A%E5%8F%8C%E7%AB%AF%E9%98%9F%E5%88%97%EF%BC%8C0%20%E6%94%BE%E9%98%9F%E5%A4%B4%201%20%E6%94%BE%E9%98%9F%E5%B0%BE%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ○ | [LC 1368 Minimum Cost to Make at Least One Valid Path in a Grid](zero-one-bfs%20%280-1%20BFS%EF%BC%9A%E5%8F%8C%E7%AB%AF%E9%98%9F%E5%88%97%EF%BC%8C0%20%E6%94%BE%E9%98%9F%E5%A4%B4%201%20%E6%94%BE%E9%98%9F%E5%B0%BE%29/LC-1368%20-%20Minimum%20Cost%20to%20Make%20at%20Least%20One%20Valid%20Path%20in%20a%20Grid) | 每格有默认方向，改方向花 1，最少花多少到终点 | 0-1 BFS：顺着方向走代价 0 放队头，改方向代价 1 放队尾 |
| ○ | [LC 2290 Minimum Obstacle Removal to Reach Corner](zero-one-bfs%20%280-1%20BFS%EF%BC%9A%E5%8F%8C%E7%AB%AF%E9%98%9F%E5%88%97%EF%BC%8C0%20%E6%94%BE%E9%98%9F%E5%A4%B4%201%20%E6%94%BE%E9%98%9F%E5%B0%BE%29/LC-2290%20-%20Minimum%20Obstacle%20Removal%20to%20Reach%20Corner) | 最少拆几个障碍到终点 | 0-1 BFS，障碍格代价 1 |
| ○ | [LC 3552 Grid Teleportation Traversal](zero-one-bfs%20%280-1%20BFS%EF%BC%9A%E5%8F%8C%E7%AB%AF%E9%98%9F%E5%88%97%EF%BC%8C0%20%E6%94%BE%E9%98%9F%E5%A4%B4%201%20%E6%94%BE%E9%98%9F%E5%B0%BE%29/LC-3552%20-%20Grid%20Teleportation%20Traversal) | 网格里有传送门（同字母之间免费瞬移） | 0-1 BFS：传送边权 0、普通移动 1，每种字母只用一次 |

## [bellman-ford (Bellman-Ford：限制 k 条边，每轮用快照)](bellman-ford%20%28Bellman-Ford%EF%BC%9A%E9%99%90%E5%88%B6%20k%20%E6%9D%A1%E8%BE%B9%EF%BC%8C%E6%AF%8F%E8%BD%AE%E7%94%A8%E5%BF%AB%E7%85%A7%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 787 Cheapest Flights Within K Stops](bellman-ford%20%28Bellman-Ford%EF%BC%9A%E9%99%90%E5%88%B6%20k%20%E6%9D%A1%E8%BE%B9%EF%BC%8C%E6%AF%8F%E8%BD%AE%E7%94%A8%E5%BF%AB%E7%85%A7%29/LC-0787%20-%20Cheapest%20Flights%20Within%20K%20Stops%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 最多转 k 次的最便宜航班 | Bellman-Ford 跑 k+1 轮、每轮用快照签名题。Dijkstra 直接做会错，要能解释为什么 |

## [floyd (Floyd：所有点对，点 ≤ 100)](floyd%20%28Floyd%EF%BC%9A%E6%89%80%E6%9C%89%E7%82%B9%E5%AF%B9%EF%BC%8C%E7%82%B9%20%E2%89%A4%20100%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 1334 Find the City With the Smallest Number of Neighbors at a Threshold Distance](<dijkstra/01 - Dijkstra 标准加法最短路/02 - LC-1334 - Find the City With the Smallest Number of Neighbors at a Threshold Distance>) | 点数 ≤ 100，每个城市在阈值内能到几个城市 | Floyd 签名题 |
| ○ | [LC 2976 Minimum Cost to Convert String I](<dijkstra/01 - Dijkstra 标准加法最短路/04 - LC-2976 - Minimum Cost to Convert String I>) | 字符转换有代价，整串最少花多少 | 26 个字母上跑 Floyd |

---

每题文件夹：`solution.py`（所有解法 + 复杂度 + ⭐ 最优）、`problem.pdf` / `problem_dark.pdf`、`metadata.json`（复习记录）。
模板在 [00-foundations/templates (模板)](../00-foundations%20%28%E5%9B%BE%E8%AE%BA%E5%9F%BA%E7%A1%80%E3%80%81%E5%9B%BE%E8%AE%BA%E6%89%8B%E5%86%8C%29/templates%20%28%E6%A8%A1%E6%9D%BF%29)，总表在 [../README.md](../README.md)。
