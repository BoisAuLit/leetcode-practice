# 00 - GRAPH ALGORITHM INDEX（算法 → 题目 反向索引）

- 题目只存一次：按「题目在问什么」放在 `01`–`12` / `99`。
- 每个一级目录里的 `00 - Recognition.md` 是正向索引：题目特征 → 问题类型 → 算法。
- 这个文件是反向索引：算法 → 它能解决的问题类型 → 本仓库里的题。

## DFS
| 用途 | 题目（目录） |
|---|---|
| Reachability / Traversal | `01` 1971 (A 递归 / B 栈) · 0133 Clone Graph · 0130 Surrounded Regions · 0417 Pacific Atlantic |
| Connected Components / Flood fill | `02` 0200 · 0695 · 0323-B |
| Undirected cycle (parent tracking) | `03/Undirected` 0261-B · 0684-A |
| Directed cycle (3-state WHITE/GRAY/BLACK) | `03/Directed` 0207-A · `10` 1059 |
| Topological sort (reversed post-order) | `04` 0210-A |
| Backtracking all paths | `10` 0797-A/B |
| Eulerian path (Hierholzer = 边消耗式 DFS) | `09` 0332 |
| Recursion on nested data | `12` 0339 · `99` 0761 |
| Templates | `00 - Foundations/03`, `04` |

## BFS
| 用途 | 题目（目录） |
|---|---|
| Reachability | `01` 1971-C/E |
| Connected Components | `02` 0200 · 0695 · 0323-C |
| Unweighted shortest path | `05` 1091 · 0127 · 3552 |
| Multi-source BFS | `11` 0994 · 0286 · 0934 · 0317 · `01` 0130 · 0417 |
| Level-order traversal | `11` 0429 · 0116 · `12` 0364 · 0339 |
| Kahn topological sort (in-degree) | `04` 0210-B · 0269 · 1136 · 0310 (leaf peeling) · `03/Directed` 0207-B |
| Undirected cycle (parent tracking) / leaf peeling | `03/Undirected` 0261-C · 0684-B |
| Bounded-edge relaxation (k+1 layers) | `06/03` 0787-A/G |
| Template | `00 - Foundations/05` |

## Union-Find (Disjoint Set)
| 用途 | 题目（目录） |
|---|---|
| Template | `08/00 - UnionFind Template.py` |
| Connectivity / Reachability | `01` 1971-D/F |
| Components | `02` 0547 · 0323-A |
| Undirected cycle / valid tree | `03/Undirected` 0261-A（0684 的经典 UF 解尚未写） |
| Dynamic connectivity / grouping | `08` 1101 · 1202 |
| Kruskal MST | `07/Kruskal` 1584 |
| Weighted UF (ratios) | `archive/004` (0399) |

完整清单见 `08 - Union-Find/Union-Find Applications.md`。

## Dijkstra
| 用途 | 题目（目录） |
|---|---|
| Non-negative weighted SSSP | `06/01` 0743 |
| + state (stops) for ≤ k edges | `06/03` 0787-D/F |
| Minimax path (relax 用 max) | `06/04` 1631 |

## Bellman-Ford / SPFA
| 用途 | 题目（目录） |
|---|---|
| Negative-weight SSSP · negative cycle | `06/02` DP 讲解 + SPFA demo |
| ≤ k edges (k+1 rounds, 用上一轮 copy) | `06/03` 0787-B/C/E（分层 BFS 形式 0787-A/G） |

## Topological Sort
| 用途 | 题目（目录） |
|---|---|
| DFS post-order | `04` 0210-A（0207-A 只判环） |
| Kahn (in-degree) | `04` 0210-B · 0269 · 1136 · `03/Directed` 0207-B |
| Leaf peeling（无向树上的 Kahn） | `04` 0310 · `03/Undirected` 0684-B |

## MST
| 算法 | 题目（目录） |
|---|---|
| Kruskal (sort edges + Union-Find) | `07/Kruskal (uses Union-Find)` 1584-A/B · 1168（虚拟节点；旧解 `archive/005`） |
| Prim (heap) | `07/Prim` 1584-A/B · 1168 Solution2（`archive/005`） |

## Eulerian Path
| 算法 | 题目（目录） |
|---|---|
| Hierholzer | `09` 0332（递归 / 迭代） |

## Greedy / degree counting（不算经典图算法）
| 技巧 | 题目（目录） |
|---|---|
| Candidate elimination | `99` 0277 |
| In/out-degree counting | `99` 0997 |

## 10 秒决策（问题 → 算法）
```text
能不能到？            → DFS / BFS（多次查询 → Union-Find）
有几块？              → DFS / BFS / Union-Find
有没有环？            → undirected: Union-Find / DFS+parent · directed: DFS 3-state / Kahn
有 dependency 求顺序？ → Topological Sort (Kahn / DFS)
最短路？              → unweighted: BFS · ≥0: Dijkstra · negative: Bellman-Ford · ≤k edges: Bellman-Ford k+1 轮 · minimax: Dijkstra+max
最便宜连接所有点？     → MST (Kruskal 稀疏 / Prim 稠密)
每条边恰好一次？       → Eulerian → Hierholzer
返回所有路径？         → DFS + backtracking
多源同时扩散 / 分层？   → Multi-source / level BFS
动态连通性？           → Union-Find
```
