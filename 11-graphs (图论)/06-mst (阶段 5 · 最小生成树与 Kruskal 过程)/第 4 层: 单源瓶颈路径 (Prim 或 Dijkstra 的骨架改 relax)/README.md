# 第 4 层: 单源瓶颈路径 (Prim 或 Dijkstra 的骨架改 relax)

**这一层没有自己的题目文件夹，题在阶段 4。** 原因：这一层和第 3 层问的是同一批题（778、1631、1102），只是换了一种解法。一道题在题库里只能有一个文件夹，否则复习队列会把同一道题抽两次。

题目在 [../../05-shortest-path (阶段 4 · 带权最短路)/bottleneck-path (瓶颈路径：relax 改 max 或 min)](../../05-shortest-path%20%28%E9%98%B6%E6%AE%B5%204%20%C2%B7%20%E5%B8%A6%E6%9D%83%E6%9C%80%E7%9F%AD%E8%B7%AF%29/bottleneck-path%20%28%E7%93%B6%E9%A2%88%E8%B7%AF%E5%BE%84%EF%BC%9Arelax%20%E6%94%B9%20max%20%E6%88%96%20min%29)，三道题的 `solution.py` 里第 3 层和第 4 层的解法都写了：

| 题 | Solution 1 (本层) | Solution 2 (第 3 层) | Solution 3 |
|---|---|---|---|
| LC-1631 Path With Minimum Effort | Dijkstra 改 relax 为 `max(d, w)` | Kruskal 过程 + 并查集 | 二分答案 + BFS |
| NC Swim in Rising Water (LC-778) | Dijkstra 改 relax 为 `max(d, grid[nx][ny])` | Kruskal 过程 (格子按高度开放) | 二分水位 + DFS |
| LC-1102 Path With Maximum Minimum Value | Dijkstra 改 relax 为 `min(d, w)` + 大根堆 | Kruskal 过程 (按值从大到小开放) | 二分答案 + BFS |

## 这一层讲的是什么

Prim、Dijkstra、最小瓶颈路径**共用一副骨架**，只有 relax 那一行不一样，因为"标签"的含义不一样：

| 算法 | 标签的含义 | 从 u 到邻居 v 的新标签 |
|---|---|---|
| Prim | 把 v 拉进圈最便宜的一根线 | `w` |
| Dijkstra | 从起点到 v 的最短总路程 | `d + w` |
| 最小瓶颈 (minimax) | 从起点到 v 的路径上最大边最小是多少 | `max(d, w)` |
| 最大最小 (maximin) | 从起点到 v 的路径上最小边最大是多少 | `min(d, w)`，配大根堆（标签取负） |

为什么 `max(d, w)` 是对的：到 u 为止路径的瓶颈是 d，再走一条价格 w 的边，新路径的瓶颈就是两者的较大者。堆每次弹最小标签，等于每次确定"目前瓶颈最小的那个点"，和 Dijkstra 每次确定"目前最近的点"是同一个道理。

## 怎么选第 3 层还是第 4 层

- **单起点单终点** → 本层（代码最短）。
- **多组查询、要离线、或者要反着时间走** → 第 3 层的 Kruskal 过程。

面试时这三题能说出三种解法并解释取舍是加分项。

模板见 [../../00-foundations (图论基础、图论手册)/templates (模板)/08 - Dijkstra 堆版 - relax 写 d + w (签名题 LC-743).py](../../00-foundations%20%28%E5%9B%BE%E8%AE%BA%E5%9F%BA%E7%A1%80%E3%80%81%E5%9B%BE%E8%AE%BA%E6%89%8B%E5%86%8C%29/templates%20%28%E6%A8%A1%E6%9D%BF%29/08%20-%20Dijkstra%20%E5%A0%86%E7%89%88%20-%20relax%20%E5%86%99%20d%20%2B%20w%20%28%E7%AD%BE%E5%90%8D%E9%A2%98%20LC-743%29.py)，详解见手册第四篇 [13 - 图论手册 - 4 - MST 五层详解](../../00-foundations%20%28%E5%9B%BE%E8%AE%BA%E5%9F%BA%E7%A1%80%E3%80%81%E5%9B%BE%E8%AE%BA%E6%89%8B%E5%86%8C%29/13%20-%20%E5%9B%BE%E8%AE%BA%E6%89%8B%E5%86%8C%20-%204%20-%20MST%20%E4%BA%94%E5%B1%82%E8%AF%A6%E8%A7%A3%20%28%E7%BB%93%E6%9E%9C%20vs%20%E8%BF%87%E7%A8%8B%29.md) 的「第四层」。
