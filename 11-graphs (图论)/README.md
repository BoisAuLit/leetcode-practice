# 11-graphs (图论) 总表

图论题不管故事怎么编，问的永远是五件事之一。拿到题先答这五个问题，答案直接给出阶段和模板：

1. 点是什么、边是什么？（建图，包括隐式图和状态图）
2. 边有权吗？全相等吗？有负权吗？
3. 图是静态的还是边会一条条来？
4. 有方向吗？题目问的是顺序或依赖吗？
5. 题目要的是：能不能到 / 最短 / 最省 / 顺序 / 结构？

| 问题 | 题目的问法 | 无权 / 静态时 | 有权 / 动态 / 有约束时 | 阶段文件夹 |
|---|---|---|---|---|
| ① 连通性 | 能不能到、有几块、怎么分组 | DFS / BFS | 边一条条加进来：Union-Find | 阶段 0、1（静态）· 阶段 2（动态） |
| ② 最短路 | A 到 B 最少步数 / 最小代价 | BFS | 非负权：Dijkstra；限制 k 条边：Bellman-Ford；所有点对且点少：Floyd；权只有 0/1：0-1 BFS | 阶段 1（无权）· 阶段 4（带权） |
| ③ 最小生成树 | 把所有点连通、总代价最小 | — | Kruskal / Prim；Kruskal 的过程还能解瓶颈路径、离线阈值查询 | 阶段 5 |
| ④ 顺序与依赖 | 先后顺序、能否全部完成、有向图有没有环 | Kahn（BFS）/ 三色 DFS | 同左 | 阶段 3 |
| ⑤ 特殊结构 | 能否分两组、删哪条边会断、欧拉路径 | 二分图染色、Tarjan 桥、Hierholzer | 面试出现频率低 | 阶段 6 |

**DFS/BFS 够用的充分条件**：边没有权（或全相等）+ 图是静态的 + 问的是连通或步数。三个条件破一个就换工具：边有权 → Dijkstra 家族或 MST；图会变 → Union-Find；有方向且问顺序 → 拓扑排序。

## 阶段 ↔ 文件夹

| 阶段 | 文件夹 | 签名题 ★ |
|---|---|---|
| 0 | [01-graph-modeling (阶段 0 · 建图、隐式图、状态图)](01-graph-modeling%20%28%E9%98%B6%E6%AE%B5%200%20%C2%B7%20%E5%BB%BA%E5%9B%BE%E3%80%81%E9%9A%90%E5%BC%8F%E5%9B%BE%E3%80%81%E7%8A%B6%E6%80%81%E5%9B%BE%29) | [1971 Find if Path Exists in Graph](01-graph-modeling%20%28%E9%98%B6%E6%AE%B5%200%20%C2%B7%20%E5%BB%BA%E5%9B%BE%E3%80%81%E9%9A%90%E5%BC%8F%E5%9B%BE%E3%80%81%E7%8A%B6%E6%80%81%E5%9B%BE%29/adjacency-list%20%28%E6%98%BE%E5%BC%8F%E5%BB%BA%E5%9B%BE%EF%BC%9A%E8%BE%B9%E5%88%97%E8%A1%A8%20%E2%86%92%20%E9%82%BB%E6%8E%A5%E8%A1%A8%29/LC-1971%20-%20Find%20if%20Path%20Exists%20in%20Graph%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98)、[133 Clone Graph](01-graph-modeling%20%28%E9%98%B6%E6%AE%B5%200%20%C2%B7%20%E5%BB%BA%E5%9B%BE%E3%80%81%E9%9A%90%E5%BC%8F%E5%9B%BE%E3%80%81%E7%8A%B6%E6%80%81%E5%9B%BE%29/adjacency-list%20%28%E6%98%BE%E5%BC%8F%E5%BB%BA%E5%9B%BE%EF%BC%9A%E8%BE%B9%E5%88%97%E8%A1%A8%20%E2%86%92%20%E9%82%BB%E6%8E%A5%E8%A1%A8%29/LC-0133%20-%20Clone%20Graph%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98)、[752 Open the Lock](01-graph-modeling%20%28%E9%98%B6%E6%AE%B5%200%20%C2%B7%20%E5%BB%BA%E5%9B%BE%E3%80%81%E9%9A%90%E5%BC%8F%E5%9B%BE%E3%80%81%E7%8A%B6%E6%80%81%E5%9B%BE%29/state-graph-bfs%20%28%E7%8A%B6%E6%80%81%E5%9B%BE%20BFS%EF%BC%9A%E4%B8%80%E4%B8%AA%E7%8A%B6%E6%80%81%E5%B0%B1%E6%98%AF%E4%B8%80%E4%B8%AA%E7%82%B9%29/LC-0752%20-%20Open%20the%20Lock%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) |
| 1 | [02-dfs-bfs (阶段 1 · DFS、BFS：静态无权的连通性与步数)](02-dfs-bfs%20%28%E9%98%B6%E6%AE%B5%201%20%C2%B7%20DFS%E3%80%81BFS%EF%BC%9A%E9%9D%99%E6%80%81%E6%97%A0%E6%9D%83%E7%9A%84%E8%BF%9E%E9%80%9A%E6%80%A7%E4%B8%8E%E6%AD%A5%E6%95%B0%29) | [200 Number of Islands](02-dfs-bfs%20%28%E9%98%B6%E6%AE%B5%201%20%C2%B7%20DFS%E3%80%81BFS%EF%BC%9A%E9%9D%99%E6%80%81%E6%97%A0%E6%9D%83%E7%9A%84%E8%BF%9E%E9%80%9A%E6%80%A7%E4%B8%8E%E6%AD%A5%E6%95%B0%29/flood-fill%20%28%E6%B4%AA%E6%B0%B4%E5%A1%AB%E5%85%85%EF%BC%9A%E6%95%B0%E8%BF%9E%E9%80%9A%E5%9D%97%29/LC-0200%20-%20Number%20of%20Islands%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98)、[417 Pacific Atlantic Water Flow](02-dfs-bfs%20%28%E9%98%B6%E6%AE%B5%201%20%C2%B7%20DFS%E3%80%81BFS%EF%BC%9A%E9%9D%99%E6%80%81%E6%97%A0%E6%9D%83%E7%9A%84%E8%BF%9E%E9%80%9A%E6%80%A7%E4%B8%8E%E6%AD%A5%E6%95%B0%29/boundary-first%20%28%E8%BE%B9%E7%95%8C%E4%BC%98%E5%85%88%EF%BC%9A%E4%BB%8E%E8%BE%B9%E7%95%8C%E5%8F%8D%E5%90%91%20DFS%29/LC-0417%20-%20Pacific%20Atlantic%20Water%20Flow%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98)、[994 Rotting Oranges](02-dfs-bfs%20%28%E9%98%B6%E6%AE%B5%201%20%C2%B7%20DFS%E3%80%81BFS%EF%BC%9A%E9%9D%99%E6%80%81%E6%97%A0%E6%9D%83%E7%9A%84%E8%BF%9E%E9%80%9A%E6%80%A7%E4%B8%8E%E6%AD%A5%E6%95%B0%29/multi-source-bfs%20%28%E5%A4%9A%E6%BA%90%20BFS%EF%BC%9A%E6%89%80%E6%9C%89%E8%B5%B7%E7%82%B9%E4%B8%80%E8%B5%B7%E5%85%A5%E9%98%9F%29/LC-0994%20-%20Rotting%20Oranges%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) |
| 2 | [03-union-find (阶段 2 · 并查集：动态加边的连通性)](03-union-find%20%28%E9%98%B6%E6%AE%B5%202%20%C2%B7%20%E5%B9%B6%E6%9F%A5%E9%9B%86%EF%BC%9A%E5%8A%A8%E6%80%81%E5%8A%A0%E8%BE%B9%E7%9A%84%E8%BF%9E%E9%80%9A%E6%80%A7%29) | [323 Number of Connected Components in an Undirected Graph](03-union-find%20%28%E9%98%B6%E6%AE%B5%202%20%C2%B7%20%E5%B9%B6%E6%9F%A5%E9%9B%86%EF%BC%9A%E5%8A%A8%E6%80%81%E5%8A%A0%E8%BE%B9%E7%9A%84%E8%BF%9E%E9%80%9A%E6%80%A7%29/count-components%20%28%E8%AE%A1%E6%95%B0%EF%BC%9A%E5%9D%97%E6%95%B0%20%3D%20n%20%E2%88%92%20%E6%88%90%E5%8A%9F%E5%90%88%E5%B9%B6%E6%AC%A1%E6%95%B0%29/LC-0323%20-%20Number%20of%20Connected%20Components%20in%20an%20Undirected%20Graph%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98)、[684 Redundant Connection](03-union-find%20%28%E9%98%B6%E6%AE%B5%202%20%C2%B7%20%E5%B9%B6%E6%9F%A5%E9%9B%86%EF%BC%9A%E5%8A%A8%E6%80%81%E5%8A%A0%E8%BE%B9%E7%9A%84%E8%BF%9E%E9%80%9A%E6%80%A7%29/cycle-by-union%20%28%E6%88%90%E7%8E%AF%EF%BC%9Aunion%20%E8%BF%94%E5%9B%9E%20False%29/LC-0684%20-%20Redundant%20Connection%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98)、[305 Number of Islands II](03-union-find%20%28%E9%98%B6%E6%AE%B5%202%20%C2%B7%20%E5%B9%B6%E6%9F%A5%E9%9B%86%EF%BC%9A%E5%8A%A8%E6%80%81%E5%8A%A0%E8%BE%B9%E7%9A%84%E8%BF%9E%E9%80%9A%E6%80%A7%29/dynamic-add%20%28%E5%8A%A8%E6%80%81%E5%8A%A0%E7%82%B9%E3%80%81%E6%8C%89%E6%97%B6%E9%97%B4%E6%8E%A8%E8%BF%9B%29/LC-0305%20-%20Number%20of%20Islands%20II%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) |
| 3 | [04-topological-sort (阶段 3 · 拓扑排序、有向图的环与依赖)](04-topological-sort%20%28%E9%98%B6%E6%AE%B5%203%20%C2%B7%20%E6%8B%93%E6%89%91%E6%8E%92%E5%BA%8F%E3%80%81%E6%9C%89%E5%90%91%E5%9B%BE%E7%9A%84%E7%8E%AF%E4%B8%8E%E4%BE%9D%E8%B5%96%29) | [207 Course Schedule](04-topological-sort%20%28%E9%98%B6%E6%AE%B5%203%20%C2%B7%20%E6%8B%93%E6%89%91%E6%8E%92%E5%BA%8F%E3%80%81%E6%9C%89%E5%90%91%E5%9B%BE%E7%9A%84%E7%8E%AF%E4%B8%8E%E4%BE%9D%E8%B5%96%29/kahn%20%28Kahn%EF%BC%9A%E6%8C%89%E5%85%A5%E5%BA%A6%E5%81%9A%20BFS%29/LC-0207%20-%20Course%20Schedule%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98)、[802 Find Eventual Safe States](04-topological-sort%20%28%E9%98%B6%E6%AE%B5%203%20%C2%B7%20%E6%8B%93%E6%89%91%E6%8E%92%E5%BA%8F%E3%80%81%E6%9C%89%E5%90%91%E5%9B%BE%E7%9A%84%E7%8E%AF%E4%B8%8E%E4%BE%9D%E8%B5%96%29/three-color-dfs%20%28%E4%B8%89%E8%89%B2%20DFS%EF%BC%9A%E9%81%87%E5%88%B0%E7%81%B0%E8%89%B2%E7%82%B9%20%3D%20%E6%9C%89%E7%8E%AF%29/LC-0802%20-%20Find%20Eventual%20Safe%20States%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) |
| 4 | [05-shortest-path (阶段 4 · 带权最短路)](05-shortest-path%20%28%E9%98%B6%E6%AE%B5%204%20%C2%B7%20%E5%B8%A6%E6%9D%83%E6%9C%80%E7%9F%AD%E8%B7%AF%29) | [743 Network Delay Time](<05-shortest-path (阶段 4 · 带权最短路)/dijkstra/01 - Dijkstra 标准加法最短路/01 - LC-0743 - Network Delay Time - 教科书>)、[787 Cheapest Flights Within K Stops](05-shortest-path%20%28%E9%98%B6%E6%AE%B5%204%20%C2%B7%20%E5%B8%A6%E6%9D%83%E6%9C%80%E7%9F%AD%E8%B7%AF%29/bellman-ford%20%28Bellman-Ford%EF%BC%9A%E9%99%90%E5%88%B6%20k%20%E6%9D%A1%E8%BE%B9%EF%BC%8C%E6%AF%8F%E8%BD%AE%E7%94%A8%E5%BF%AB%E7%85%A7%29/LC-0787%20-%20Cheapest%20Flights%20Within%20K%20Stops%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98)、[1334 Find the City With the Smallest Number of Neighbors at a Threshold Distance](<05-shortest-path (阶段 4 · 带权最短路)/dijkstra/01 - Dijkstra 标准加法最短路/02 - LC-1334 - Find the City With the Smallest Number of Neighbors at a Threshold Distance>) |
| 5 | [06-mst (阶段 5 · 最小生成树与 Kruskal 过程)](06-mst%20%28%E9%98%B6%E6%AE%B5%205%20%C2%B7%20%E6%9C%80%E5%B0%8F%E7%94%9F%E6%88%90%E6%A0%91%E4%B8%8E%20Kruskal%20%E8%BF%87%E7%A8%8B%29) | [1584 Min Cost to Connect All Points](06-mst%20%28%E9%98%B6%E6%AE%B5%205%20%C2%B7%20%E6%9C%80%E5%B0%8F%E7%94%9F%E6%88%90%E6%A0%91%E4%B8%8E%20Kruskal%20%E8%BF%87%E7%A8%8B%29/%E7%AC%AC%201%20%E5%B1%82%3A%20%E4%BC%AA%E8%A3%85%E6%88%90%E5%88%AB%E7%9A%84%E6%95%85%E4%BA%8B%E7%9A%84%20MST%28%E5%BB%BA%E6%A8%A1%E9%A2%98%29/LC-1584%20-%20Min%20Cost%20to%20Connect%20All%20Points%20-%20%E7%BA%AF%E7%B2%B9%E7%9A%84%20MST%20-%20%E7%A8%A0%E5%AF%86%E5%9B%BE%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98)、[1697 Checking Existence of Edge Length Limited Paths](06-mst%20%28%E9%98%B6%E6%AE%B5%205%20%C2%B7%20%E6%9C%80%E5%B0%8F%E7%94%9F%E6%88%90%E6%A0%91%E4%B8%8E%20Kruskal%20%E8%BF%87%E7%A8%8B%29/%E7%AC%AC%203%20%E5%B1%82%3A%20%E7%93%B6%E9%A2%88%E8%B7%AF%E5%BE%84%E4%B8%8E%E9%98%88%E5%80%BC%E8%BF%9E%E9%80%9A%20%28%E7%94%A8%20Kruskal%20%E7%9A%84%E8%BF%87%E7%A8%8B%2C%20%E4%B8%8D%E8%A6%81%E6%A0%91%29/LC-1697%20-%20Checking%20Existence%20of%20Edge%20Length%20Limited%20Paths%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) |
| 6 | [07-special-structures (阶段 6 · 特殊结构)](07-special-structures%20%28%E9%98%B6%E6%AE%B5%206%20%C2%B7%20%E7%89%B9%E6%AE%8A%E7%BB%93%E6%9E%84%29) | [785 Is Graph Bipartite?](07-special-structures%20%28%E9%98%B6%E6%AE%B5%206%20%C2%B7%20%E7%89%B9%E6%AE%8A%E7%BB%93%E6%9E%84%29/bipartite%20%28%E4%BA%8C%E5%88%86%E5%9B%BE%E6%9F%93%E8%89%B2%29/LC-0785%20-%20Is%20Graph%20Bipartite%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98)、[1192 Critical Connections in a Network](07-special-structures%20%28%E9%98%B6%E6%AE%B5%206%20%C2%B7%20%E7%89%B9%E6%AE%8A%E7%BB%93%E6%9E%84%29/tarjan-bridges%20%28Tarjan%20%E6%B1%82%E6%A1%A5%E3%80%81%E5%89%B2%E7%82%B9%29/LC-1192%20-%20Critical%20Connections%20in%20a%20Network%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) |

基础资料、图论手册（Claude Desktop 整理的六篇）、算法模板都在 [00-foundations (图论基础、图论手册)](00-foundations%20%28%E5%9B%BE%E8%AE%BA%E5%9F%BA%E7%A1%80%E3%80%81%E5%9B%BE%E8%AE%BA%E6%89%8B%E5%86%8C%29)。

## 三条"只改一行"的记忆线

- **遍历链**：DFS → BFS → 多源 BFS → 0-1 BFS → Dijkstra → Bellman-Ford → Floyd。都是"松弛"，区别只在松弛的顺序：队列按层 / 双端队列 / 堆按距离 / 所有边轮流 V−1 轮 / 按中转点三层循环。
- **生成树链**：Prim 和 Dijkstra 是同一副骨架，只差 relax 写 `w` 还是 `d + w`；Kruskal = 排序 + Union-Find。
- **有向图链**：Kahn 就是"按入度做 BFS"；DFS 后序倒过来就是拓扑序；三色 DFS 是"DFS 遇到灰色点 = 有环"。

## 刷题路线（核心线，顺序即优先级）

- **阶段 0**：1971 → 133 → 752 → 127 → 797 → 1466
- **阶段 1**：200 → 695 → 994 → 542 → 417 → 130 → 1254 → 547 → 1091
- **阶段 2**：323 → 684 → 1319 → 305 → 721 → 990 → 947 → 1101
- **阶段 3**：207 → 210 → 802 → 310 → 269 → 1136 → 329
- **阶段 4**：743 → 1514 → 1631 → 1368 → 787 → 1334 → 1976
- **阶段 5**：1584（三种写法） → 1489 → 1697 → 1970
- **阶段 6**：785 → 1192 → 332

近期有面试：先把 200、994、417、323、684、207、802、743、787 这九道签名题一周内过完，它们覆盖八成的图论面试题。
核心线做完后按最弱的阶段回头补 ○，最后才碰 △；△ 里优先 827、2050、2577（并查集 + 枚举、拓扑 + DP、Dijkstra + 状态）。

## 每道题怎么做

1. 动手前先答上面五个问题，说出它属于哪个阶段、用哪个签名题的模板。
2. 做完在 `solution.py` 文件头写一行"和签名题比改了哪一行"。改动写不出来，说明还没真正归类。
3. 复习：`shuffle` 抽到图论题时只看 `solution_retry.py` 里的 banner（解法名 + 复杂度）盲写，写不出来再看 `solution.py`。
4. 每个阶段结束做一次出关测试（各阶段 README 第一段），没过就不进下一阶段。

---

# 本次重构补充说明（2026-11-11）

> 上面的原有内容（阶段 0–6 的知识地图、决策树、模板）**一字未改**。
> 下面是本次按 `instructions.md` 执行后新增的说明。

## 一、8 个 Level 1 与现有阶段目录的对应

instructions.md 建议建立 8 个 Level 1。**现有的阶段目录本身就是这 8 个 Level 1**，
只是名字带着「阶段 N」的学习顺序标记。**本次刻意没有改目录名**，理由有三条：

1. instructions.md 自己要求「请优先保留原有阶段式学习逻辑」。
2. 项目的 **`.claude/skills/intake`** 技能里**直接写着这些路径**作为入库示例
   （例如 `11-graphs (图论)/02-dfs-bfs (阶段 1 · …)/multi-source-bfs (…)`）。改名会让该技能失效。
3. 其他专题的 README 里已经有**十几条**指向这些路径的跨专题链接
   （04-stack-queue、06-linked-list、07-trees 都引用了图论的目录）。

| instructions 的 Level 1 | 对应的现有目录 |
|---|---|
| 01 图建模与基础遍历 | `01-graph-modeling (阶段 0 · 建图、隐式图、状态图)` |
| 02 DFS BFS 与无权最短路 | `02-dfs-bfs (阶段 1 · …)` |
| 03 Union-Find 与连通性 | `03-union-find (阶段 2 · …)` |
| 04 Topological Sort 与 DAG | `04-topological-sort (阶段 3 · …)` |
| 05 带权最短路 | `05-shortest-path (阶段 4 · …)` |
| 06 最小生成树与离线阈值连通 | `06-mst (阶段 5 · …)` |
| 07 特殊图结构与路径 | `07-special-structures (阶段 6 · …)` |
| 08 函数图与树上图论 | 拆在 `02-dfs-bfs/functional-graph` 和 `07-special-structures/tree-problems` 两处 |

**关于 Level 1 `08`**：函数图（每点一条出边）本质是「阶段 1 的 DFS 特例」，
树上问题本质是「阶段 6 的特殊结构」。把它们单独拎出来做第 8 个 Level 1
会和现有的阶段逻辑冲突，所以保留在原位，并在这里登记它们的位置。

## 二、六组「同题多算法」的归属（本次重点处理）

这六个 LC 编号各有**两份不同算法**的实现。**两份都保留，一个字节都没删**，
但为了让复习队列里一道题只出现一次，**非主位置的目录改名成「变体 · …」**
（不再匹配 `LC-xxxx - ` 前缀，所以 `review_due.py` 不会重复排它），
并把它的实现**并进主位置的 solution.py** 作为 `Solution_*_Alt` 方便对照。

| LC | Primary Pattern | Primary Path | Alternative Pattern | Alternative Path（已改名） | 为什么这样定主次 |
|---|---|---|---|---|---|
| **0787** | Bellman-Ford + Snapshot | [`bellman-ford/LC-0787 … ★ 签名题`](<05-shortest-path (阶段 4 · 带权最短路)/bellman-ford (Bellman-Ford：限制 k 条边，每轮用快照)/LC-0787 - Cheapest Flights Within K Stops - ★ 签名题>) | Dijkstra 状态扩展 | `dijkstra/05 - …/变体 · 01 - LC-0787 …` | instructions：「本专题优先推荐 Bellman-Ford + Snapshot」 |
| **1368** | 0-1 BFS | [`zero-one-bfs/LC-1368 …`](<05-shortest-path (阶段 4 · 带权最短路)/zero-one-bfs (0-1 BFS：双端队列，0 放队头 1 放队尾)/LC-1368 - Minimum Cost to Make at Least One Valid Path in a Grid>) | Dijkstra（优先队列） | `dijkstra/04 - …/变体 · 02 - LC-1368 …` | 边权只有 0/1 ⟹ 0-1 BFS 是 O(V+E)，Dijkstra 多一个 log |
| **2290** | 0-1 BFS | [`zero-one-bfs/LC-2290 …`](<05-shortest-path (阶段 4 · 带权最短路)/zero-one-bfs (0-1 BFS：双端队列，0 放队头 1 放队尾)/LC-2290 - Minimum Obstacle Removal to Reach Corner>) | Dijkstra | `dijkstra/04 - …/变体 · 01 - LC-2290 …` | 同 LC-1368 |
| **1334** | Dijkstra（每点各跑一次） | [`dijkstra/01/02 - LC-1334 …`](<05-shortest-path (阶段 4 · 带权最短路)/dijkstra/01 - Dijkstra 标准加法最短路/02 - LC-1334 - Find the City With the Smallest Number of Neighbors at a Threshold Distance>) | Floyd-Warshall | `floyd/变体 · LC-1334 … ★ 签名题` | instructions：「Floyd 是 P2 参考分类，不作为核心记忆；更希望用重复跑 Dijkstra 来理解」 |
| **2976** | Dijkstra | [`dijkstra/01/04 - LC-2976 …`](<05-shortest-path (阶段 4 · 带权最短路)/dijkstra/01 - Dijkstra 标准加法最短路/04 - LC-2976 - Minimum Cost to Convert String I>) | Floyd-Warshall | `floyd/变体 · LC-2976 …` | 同 LC-1334 |
| **1631** | Dijkstra 非加法代价（Minimax） | [`dijkstra/02/01 - LC-1631 …`](<05-shortest-path (阶段 4 · 带权最短路)/dijkstra/02 - Dijkstra 非加法路径代价变体/01 - LC-1631 - Path With Minimum Effort>) | 瓶颈路径模板（relax 改 max） | `bottleneck-path/变体 · LC-1631 …` | instructions 把它列在 Dijkstra 子树的「非加法路径代价变体」作为主学习位置 |

> **这六组绝对不是重复文件。** Bellman-Ford / Dijkstra / 0-1 BFS / Floyd / 瓶颈路径
> 是五种不同的算法，判断去重时依据的是**文件实际内容**而不是 LC 编号。
> 变体目录里的 `problem.pdf`、`metadata.json`、笔记全部原地保留。

**代价**：变体目录不再被 `tools/update_path.sh` 维护（它只认题目前缀），
所以那些 `metadata.json` 里的 `path` 字段会停留在改名前的值。这是有意的取舍 ——
变体目录不参与复习调度，`path` 不准确不影响任何工具。

## 三、本次新增的 6 道题

**第一轮 4 道**（instructions 指定）：

| LC | 放在哪 | 为什么放这里 |
|---|---|---|
| **LC-1293** Shortest Path in a Grid with Obstacles Elimination | `01-graph-modeling/state-graph-bfs` | 点是 `(r, c, 已用清除次数)` —— 资源压进状态后边权恢复成 1，裸 BFS 即可。和签名题 LC-0752 同族 |
| **LC-0815** Bus Routes | `01-graph-modeling/adjacency-list` | **点是「路线」不是「车站」**。选错点就做不出来，是建图题最好的教材 |
| **LC-0959** Regions Cut By Slashes | `03-union-find/modeling` | 把每个格子**切成 4 个三角形**当点 —— 「点不一定是题目字面给的东西」的极致例子 |
| **LC-2192** All Ancestors of a Node in a DAG | `04-topological-sort/kahn` | 沿拓扑序传播「祖先集合」，是 DAG 上传播信息的通用骨架 |

**第二轮自主新增 2 道**（上限 4，没有凑数）：

| LC | 放在哪 | 为什么值得加 |
|---|---|---|
| **LC-0847** Shortest Path Visiting All Nodes | `01-graph-modeling/state-graph-bfs` | 状态里带的是**一个集合**（位掩码），而不是一个标量资源。这是状态压缩的入口、通往状压 DP 的桥。本专题原本没有这个视角 |
| **LC-1519** Number of Nodes in the Sub-Tree With the Same Label | `07-special-structures/tree-problems` | 练「**子树统计量自底向上合并**」这个树上最通用的骨架，并演示了「小表合并进大表」和「迭代 DFS 防爆栈」两个工程细节 |

**审核过、决定不加**：LC-0924（Union-Find + 恶意软件，和现有并查集题技能重合）、
LC-1263（Minimum Moves to Move a Box，状态是 `(箱子位置, 人位置)` 的双层 BFS，
学习成本远高于收益）、LC-0684（已有，禁止重复）、LC-1631（已有，禁止重复）。

## 四、NC-only 题目正式化

| 原 NC | 升格为 | 处理 |
|---|---|---|
| `NC - Longest Increasing Path in Matrix` | **LC-0329 - Longest Increasing Path in a Matrix** | 目录改名 + `metadata.id` 改为 `LC-0329` + 补上官方 leetcode 链接。`practice` 原为空，无记录损失 |

**特别保留**：`asset-NC-07 - LC-0329 - Explanation.jpg` 原位未动。
归属：`04-topological-sort/dag-dp (DAG 上的 DP)` —— 它的推荐解法正是
**DFS + Memoization**（等价于在隐式 DAG 上做记忆化搜索，因为「严格递增」保证了无环）。

本次**没有建 `_neetcode/` 子目录**：仓库现行规则是「LC / NC 重复时只保留 LeetCode 版」，
而这道题是孤儿 NC（没有对应的 LC 目录），所以是**升格**而不是归档。

## 五、修复的 13 条死链

本专题原有 **13 条失效的 README 相对链接**（指向更早一次 dijkstra 重构中已改名的目录）：
- `05-shortest-path/README.md` 里 12 条（指向 `dijkstra (Dijkstra 堆版…)`、
  `dijkstra-state (Dijkstra + 状态扩展)`、`bottleneck-path/LC-1631`、`bottleneck-path/NC - Swim in Rising Water` 等）
- 根 `README.md` 里 1 条

**全部已修复**，连同本次改名产生的新链接一起，现在**死链 0**（201 条相对链接全部可达）。

## 六、校验结果

- 原始文件 524 个 → **515 个逐字节未变**，9 个有意变更（6 个主位置 solution.py 并入了变体实现，
  3 个 README 修了死链）
- `solution.py` 运行：**117 / 117 全部通过**（迁移前 111/111）
- 题目文件夹 117 个（111 原有 + 6 新增），编号连续
- 写入范围：全部在 `11-graphs (图论)/` 之内
- 未执行 `git add` / `commit` / `push`；未使用 `rm -rf`

完整审计见 [_audit/post-migration-report.md](<_audit/post-migration-report.md>)。
本次重构前的根 README 已留档为 [_audit/README.md.before-this-refactor](<_audit/README.md.before-this-refactor>)。
