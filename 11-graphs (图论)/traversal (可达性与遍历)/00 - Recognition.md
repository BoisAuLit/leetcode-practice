# Recognition — Reachability & Traversal（能不能到？能到哪些点？）

题目信号
- "is there a path from A to B" / "can reach" / "valid path" → reachability
- "visit / collect every node reachable from X" / "clone the graph" → traversal
- "cells connected to the border / to the ocean" → 从一组源出发的 reachability（反向思考：从边界出发）

候选算法
1. DFS（递归 / 栈）— 任何 reachability；需要 post-order 或回溯时首选
2. BFS（队列）— reachability，顺便得到最少步数
3. Union-Find — 多次 "A,B 连通吗？" 查询，或边是动态加入的

题目
- 1971 Find if Path Exists — DFS rec (A) / DFS stack (B) / BFS (C, E) / Union-Find (D, F)
- 0133 Clone Graph — DFS / BFS + old→copy hashmap
- 0130 Surrounded Regions — 从边界的 O 出发 BFS，没被到达的 O 全部翻转
- 0417 Pacific Atlantic — 从两个海洋反向 BFS（邻居高度 ≥ 当前），取交集

陷阱
- 入队 / 入栈时立即标记 seen
- DFS 不保证最短路径 → 要最短路去 `05`
