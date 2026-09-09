# Recognition — Unweighted Shortest Path（每走一步 cost = 1 的最短路）

题目信号
- "minimum number of steps / moves / transformations"、grid 移动、word ladder、每条边权重相同
- ⭐️ 边权全相同 → BFS，第一次出队即最短；**不要用 DFS**

模板
- queue + seen（入队时标记）；两种写法：(node, dist) 元组，或按层 `for _ in range(len(queue))`
- 隐式图：邻居现场生成（改一个字母 / 传送门）

题目
- 1091 Shortest Path in Binary Matrix — 8 方向 BFS（A 元组 / B 分层）
- 0127 Word Ladder — 单词 = 节点，改一个字母 = 边
- 3552 Grid Teleportation — 分层 BFS，传送门 0 成本（同层加入）

边界
- 有权重 → `06`；权重只有 0/1 → 0-1 BFS（deque 两端）
