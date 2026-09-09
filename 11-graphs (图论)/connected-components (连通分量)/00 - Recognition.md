# Recognition — Connected Components（图里有几块？每块多大？）

题目信号
- "number of islands / provinces / components", "largest island area", "groups of friends"

核心模板
- 遍历所有 node；每遇到一个 unseen node → component + 1，然后 DFS / BFS 把整块标完
- Union-Find：union 所有边，count = n − 成功 union 的次数

题目
- 0200 Number of Islands — grid flood fill（DFS 递归 / DFS 栈 / BFS）
- 0695 Max Area of Island — flood fill + 计数
- 0547 Number of Provinces — Union-Find on adjacency matrix
- 0323 Number of Connected Components — Union-Find (A) / DFS (B) / BFS (C)

选择
- 只要数量 / 大小 → DFS / BFS 最直接；输入是边列表且要 count → Union-Find 最短
