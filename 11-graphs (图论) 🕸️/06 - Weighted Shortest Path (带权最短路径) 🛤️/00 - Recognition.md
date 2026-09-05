# Recognition — Shortest Path（按约束选算法）

1. Unweighted / every edge same cost → **BFS**（`05` 目录）
2. Weighted + all weights ≥ 0 → **Dijkstra**（`01`）
3. Negative edges allowed → **Bellman-Ford / SPFA**（`02`）
4. At most K edges / stops → **Bellman-Ford DP**（k+1 轮，用上一轮 copy）或 state-expanded Dijkstra / BFS（`03`）
5. Minimise the largest edge on the path（minimax）→ **Dijkstra with max**（`04`）
6. All-pairs shortest path → Floyd-Warshall（本目录暂无题）

关键区别
- Dijkstra：第一次 pop 即最终距离；过期项 `if dist[node] < cost: continue`
- Bellman-Ford：第 i 轮后 = 用 ≤ i 条边的最优；必须用上一轮的 copy
- Prim 和 Dijkstra 骨架一样，但 key 是单条边权，不是累计距离（见 `07`）

题目
- 0743 Network Delay Time → Dijkstra（答案 = 最远点的距离）
- 0787 Cheapest Flights Within K Stops → BF k+1 轮 (B/E) / BF queue (C) / 分层 BFS (A/G) / Dijkstra+stops (D/F)
- 1631 Path With Minimum Effort → Dijkstra，relax 用 max
