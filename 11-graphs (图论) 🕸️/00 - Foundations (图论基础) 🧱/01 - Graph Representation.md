# Graph Representation（建图）

1. **Adjacency list**（最常用）
   ```python
   graph = defaultdict(list)
   for u, v in edges:
       graph[u].append(v)
       graph[v].append(u)        # 无向图要双向
   # 带权: graph[u].append((v, w))
   ```
2. **Adjacency matrix** — n×n；稠密图，或输入本身就是矩阵（0547 Number of Provinces）
3. **Edge list** — Kruskal（排序边）、Bellman-Ford（逐边 relax）直接在边列表上跑
4. **Implicit graph** — 网格（4/8 方向）、单词（改一个字母）、状态空间：邻居现场生成，不建图

约定
- 节点是 0..n−1 ⇒ `seen = [False] * n`；否则用 `set`
- 入队 / 入栈时**立即**标记 seen（避免重复入队）
- 模板：03 DFS 递归 · 04 DFS 迭代(栈) · 05 BFS(队列)
