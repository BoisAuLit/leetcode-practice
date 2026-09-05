# Recognition — Dependency & Topological Sort（"A 必须在 B 之前"，求顺序）

题目信号
- prerequisites / dependencies / "order in which to …" / alien dictionary letter order / "minimum semesters"
- 本质：DAG 上求线性顺序；有环 ⇒ 无解

两种模板
1. **Kahn**（BFS, in-degree）：入度 0 入队 → 出队加入 order → 邻居入度 −1 → 变 0 入队；分层计数 = 最少轮数（1136）
2. **DFS post-order**：UNVISITED / VISITING / VISITED；VISITED 后 append；最后 reverse

题目
- 0210 Course Schedule II — DFS TopSort (A) / Kahn (B)
- 0269 Alien Dictionary — 相邻单词第一个不同字母建边 → Kahn；前缀矛盾 / 环 ⇒ ""
- 1136 Parallel Courses — Kahn 分层 = 学期数
- 0310 Minimum Height Trees — 无向树上的 "Kahn"：逐层剥叶子，剩 ≤ 2 个点 = 树心

注意：是 **Kahn**，不是 Khan。理论：`00 - Theory`（William Fiset）
