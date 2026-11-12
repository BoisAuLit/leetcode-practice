# Level 1 · 06 Queue 与 BFS (Breadth-First Search)

> **Queue 是数据结构，BFS 是算法。** 本章的目的是说明「队列最重要的应用是什么」，
> **不是**把整个图论 BFS 题库搬过来。图论主线在
> [11-graphs (图论)](<../../11-graphs (图论)/README.md>)。

## 核心定义
BFS 按「距离起点的层数」逐层扩展。队列的 FIFO 保证第 d 层的节点
全部排在第 d+1 层之前，于是**每个节点第一次被访问时的距离就是最短距离**。

## 决定性观察
1. **为什么必须是 Queue**：换成 Stack 就变成 DFS，「第一次访问即最短」立刻失效。
2. **入队时就标记已访问**，不要等出队再标记 —— 否则同一个节点会被重复入队，
   复杂度退化，甚至在某些题里导致错误答案。
3. **多源 BFS**：所有起点一次性入队，等价于加一个虚拟超级源点连向所有起点。
   出队顺序依然保证按距离递增。
4. **层数 = 步数**：要么按层处理（`for _ in range(len(q))`），
   要么把距离直接写进状态 / 格子里。

## Loop Invariant
队列中的节点距离最多相差 1，且距离小的排在前面（单调不减）。

## 模板
```python
q = deque(所有起点)
for s in 所有起点: visited.add(s)
step = 0
while q:
    for _ in range(len(q)):          # 一次处理一整层
        cur = q.popleft()
        for nxt in neighbors(cur):
            if nxt not in visited:
                visited.add(nxt)     # 入队时标记，不是出队时
                q.append(nxt)
    step += 1
```
O(V + E) 时间，O(V) 空间。

## 题目（实体）

| # | 题 | 优先级 | 独有的东西 |
|---|---|---|---|
| 01/01 | LC-0733 Flood Fill | P1 | 最朴素的网格遍历；注意「新旧颜色相同」要提前返回，否则死循环 |
| 02/01 | LC-0279 Perfect Squares | P1 | 把「剩余数值」当作 BFS **状态**，每步减一个平方数，求最少步数 |

**LC-0279 的重要说明**：这题**也可以用动态规划**（`dp[i] = min(dp[i - j*j]) + 1`），
BFS 不是唯一正解。BFS 的价值在于展示「状态图上的无权最短路」这个视角：
节点是数值，边是「减去一个完全平方数」，问的是最短路径长度。

## 跨专题索引（不重复建目录）

| LC | 题 | 为什么在别处 | 位置 |
|---|---|---|---|
| 0286 | Walls and Gates | 多源 BFS 的教科书题，图论专题有更完整的版本 | [11-graphs 多源 BFS](<../../11-graphs (图论)/02-dfs-bfs (阶段 1 · DFS、BFS：静态无权的连通性与步数)/multi-source-bfs (多源 BFS：所有起点一起入队)/LC-0286 - Walls and Gates>) |
| 0994 | Rotting Oranges | 多源 BFS + 层计数的 ★ 签名题 | [11-graphs 多源 BFS](<../../11-graphs (图论)/02-dfs-bfs (阶段 1 · DFS、BFS：静态无权的连通性与步数)/multi-source-bfs (多源 BFS：所有起点一起入队)/LC-0994 - Rotting Oranges - ★ 签名题>) |
| 0752 | Open the Lock | 状态图 BFS 的 ★ 签名题 | [11-graphs 状态图 BFS](<../../11-graphs (图论)/01-graph-modeling (阶段 0 · 建图、隐式图、状态图)/state-graph-bfs (状态图 BFS：一个状态就是一个点)/LC-0752 - Open the Lock - ★ 签名题>) |

本专题原有的 LC-0286 副本（31 行的简版）已无损归档到
[`_cross_topic_archive/`](<../_cross_topic_archive>)，目录名刻意不再匹配 `LC-xxxx - ` 前缀，
因此不会在复习队列里和图论那份重复。两份的 `practice` 迁移前都是空的，没有丢失任何复习记录。

## 常见错误
- 出队时才标记 visited → 同一节点重复入队。
- LC-0733 没处理 `newColor == 原色` → 无限循环。
- 以为「队列实现的搜索」就一定是最短路 —— 只有**无权图**才成立。
  有权图要用 Dijkstra（见 11-graphs 阶段 4）。

## 复习时的 Pattern Recognition
> 「最少步数 / 最短距离 / 最少操作次数」+「每一步代价都一样」 → BFS。
> 「所有 X 同时开始扩散」 → 多源 BFS。
> 「每一步代价不同」 → 不是 BFS，去看 Dijkstra。
