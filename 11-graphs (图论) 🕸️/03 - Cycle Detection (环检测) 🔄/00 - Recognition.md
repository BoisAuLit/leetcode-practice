# Recognition — Cycle Detection（有没有环？）

先问：**有向** 还是 **无向**？

## Undirected（无向）
- 信号："is it a valid tree", "which edge can be removed", "redundant connection"
- 方法
  1. Union-Find：union(u, v) 时两端已同根 ⇒ 这条边成环（0684 的经典解）
  2. DFS / BFS 带 parent：遇到 visited 且不是 parent ⇒ 有环
  3. 树判定：n−1 条边 + 连通 ⇔ 无环 + 连通 ⇔ 树
- 题目：0261 Graph Valid Tree（UF / DFS / BFS）· 0684 Redundant Connection（DFS 逐边连通性 / leaf peeling）

## Directed（有向）
- 信号："can finish all courses", "prerequisites", "deadlock", "does every path end at t"
- 方法
  1. DFS 3-state：UNVISITED → VISITING → VISITED；碰到 VISITING ⇒ 环
  2. Kahn：processed < n ⇒ 环
- 题目：0207 Course Schedule（DFS 3-state / Kahn）· 1059 在 `10 - Enumerating & Validating Paths`
