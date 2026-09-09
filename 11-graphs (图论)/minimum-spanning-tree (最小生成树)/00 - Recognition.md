# Recognition — Minimum Spanning Tree（最便宜地把所有点连起来）

题目信号
- "connect all points / cities / houses with minimum total cost", "minimum cost to make everything connected"，无向带权图

两种算法
- **Kruskal**：边按权排序，Union-Find 判环，取 V−1 条 → 稀疏图 / 输入就是边列表
- **Prim**：heap 维护 frontier 最小边，从一个点长出来 → 稠密图 / 完全图（1584）；数组版 O(V²) 最快
- Union-Find 是 Kruskal 的零件，不是另一种 MST 算法

题目
- 1584 Min Cost to Connect All Points — Kruskal（`Kruskal (uses Union-Find)/`）与 Prim（`Prim/`）
- 1168 Optimize Water Distribution — 虚拟节点 0 把"打井"变成边，再 MST（stub，待重做；旧解在 `archive/005`）

理论：`00 - Theory`（Spanning Tree、Cut Property）· `Kruskal's.pdf` · `Prim's Algorithm.pdf`
