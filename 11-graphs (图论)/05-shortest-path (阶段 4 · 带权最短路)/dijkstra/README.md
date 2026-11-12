# Dijkstra 学习体系（18 题）

为 Silicon Valley SWE / AI Engineer 的算法面试和 OA 准备的 Dijkstra 专题。文件夹编号是**学习优先级**，不是题号。

## 先记住不变量（invariant）

Dijkstra 的唯一承诺是：**从堆里第一次弹出一个节点时，它身上的标签已经是最终答案**。

这个承诺成立的前提不是「边权为正」，而是更一般的**单调性（monotonicity）**：
沿着一条路往下接一条边，路径代价**不会变得更好**。四种代价函数都满足它，所以同一个框架能套四种题：

| 代价函数 | relaxation | 堆 | 单调性为什么成立 | 代表题 |
|---|---|---|---|---|
| 加法 Additive | `d + w` | 小根堆 | `w >= 0`，加了只会更大 | 743 |
| 最小化最大值 Minimax | `max(d, w)` | 小根堆 | 取 max 只会更大 | 1631 / 778 |
| 最大化最小值 Maximin | `min(d, w)` | 大根堆 | 取 min 只会更小 | 2812 |
| 乘法 Multiplicative | `d * w` | 大根堆 | `0 <= w <= 1`，乘了只会更小 | 1514 |

一旦这条单调性被破坏（出现负权、或者「现在多花一点以后省更多」），Dijkstra 就不成立，要么扩状态把被破坏的那一维补回来（Level 5），要么换 Bellman-Ford。

## 五层分别在练什么

| 层 | 名字 | 变的是什么 |
|---|---|---|
| 01 | Dijkstra 标准加法最短路 | 标准 Min-Heap + dist + relaxation，relax 写 `d + w`。|
| 02 | Dijkstra 非加法路径代价变体 | Greedy 框架、堆、dist 一个字不改，**只改 relaxation 和堆的方向**。|
| 03 | Dijkstra 最短路计数与结果组合 | 距离本身用标准模板算，考点在**算完之后怎么加工**：顺带计数、跑多次、跑反图。|
| 04 | Dijkstra 网格建图与特殊边权 | 点是格子、边是四方向，**不用先建邻接表**。|
| 05 | Dijkstra 状态扩展与时间约束 | `dist[node]` 不够用了：存在额外的资源维度或时间约束，必须扩状态，或者换 Bellman-Ford。|

## 18 道题（按最终目录顺序）

★ = 核心必练（必须能闭卷默写）　○ = 进阶拓展（能说清思路即可）

### 01 - Dijkstra 标准加法最短路

标准 Min-Heap + dist + relaxation，relax 写 `d + w`。这一层只练一件事：把题目翻译成图，然后原样套模板。

| | 题号 | 题目 | 难度 | 主要考点 |
|---|---|---|---|---|
| ★ | LC-0743 | [LC-0743 - Network Delay Time - 教科书](01%20-%20Dijkstra%20%E6%A0%87%E5%87%86%E5%8A%A0%E6%B3%95%E6%9C%80%E7%9F%AD%E8%B7%AF/01%20-%20LC-0743%20-%20Network%20Delay%20Time%20-%20%E6%95%99%E7%A7%91%E4%B9%A6) | M | 最标准的单源最短路；堆、dist、作废票三件套 |
| ★ | LC-1334 | [LC-1334 - Find the City With the Smallest Number of Neighbors at a Threshold Distance](01%20-%20Dijkstra%20%E6%A0%87%E5%87%86%E5%8A%A0%E6%B3%95%E6%9C%80%E7%9F%AD%E8%B7%AF/02%20-%20LC-1334%20-%20Find%20the%20City%20With%20the%20Smallest%20Number%20of%20Neighbors%20at%20a%20Threshold%20Distance) | M | 对每个点各跑一次标准 Dijkstra；n ≤ 100 时 Floyd 同样可行 |
| ○ | LC-2642 | [LC-2642 - Design Graph With Shortest Path Calculator](01%20-%20Dijkstra%20%E6%A0%87%E5%87%86%E5%8A%A0%E6%B3%95%E6%9C%80%E7%9F%AD%E8%B7%AF/03%20-%20LC-2642%20-%20Design%20Graph%20With%20Shortest%20Path%20Calculator) | H | 设计题：动态加边 + 每次查询跑一次标准 Dijkstra |
| ○ | LC-2976 | [LC-2976 - Minimum Cost to Convert String I](01%20-%20Dijkstra%20%E6%A0%87%E5%87%86%E5%8A%A0%E6%B3%95%E6%9C%80%E7%9F%AD%E8%B7%AF/04%20-%20LC-2976%20-%20Minimum%20Cost%20to%20Convert%20String%20I) | M | 建模题：26 个字母当节点，替换规则当有向边 |

### 02 - Dijkstra 非加法路径代价变体

Greedy 框架、堆、dist 一个字不改，**只改 relaxation 和堆的方向**。一层四题刚好覆盖四种代价函数。

| | 题号 | 题目 | 难度 | 主要考点 |
|---|---|---|---|---|
| ★ | LC-1631 | [LC-1631 - Path With Minimum Effort](02%20-%20Dijkstra%20%E9%9D%9E%E5%8A%A0%E6%B3%95%E8%B7%AF%E5%BE%84%E4%BB%A3%E4%BB%B7%E5%8F%98%E4%BD%93/01%20-%20LC-1631%20-%20Path%20With%20Minimum%20Effort) | M | minimax：门槛在**边**上，`relax = max(d, w)`，小根堆 |
| ★ | LC-1514 | [LC-1514 - Path with Maximum Probability](02%20-%20Dijkstra%20%E9%9D%9E%E5%8A%A0%E6%B3%95%E8%B7%AF%E5%BE%84%E4%BB%A3%E4%BB%B7%E5%8F%98%E4%BD%93/02%20-%20LC-1514%20-%20Path%20with%20Maximum%20Probability) | M | 乘法代价：`relax = d * w`，大根堆；**不是** minimax |
| ★ | LC-0778 | [LC-0778 - Swim in Rising Water](02%20-%20Dijkstra%20%E9%9D%9E%E5%8A%A0%E6%B3%95%E8%B7%AF%E5%BE%84%E4%BB%A3%E4%BB%B7%E5%8F%98%E4%BD%93/03%20-%20LC-0778%20-%20Swim%20in%20Rising%20Water) | H | minimax：门槛在**格子**上，`relax = max(d, grid[nr][nc])` |
| ○ | LC-2812 | [LC-2812 - Find the Safest Path in a Grid](02%20-%20Dijkstra%20%E9%9D%9E%E5%8A%A0%E6%B3%95%E8%B7%AF%E5%BE%84%E4%BB%A3%E4%BB%B7%E5%8F%98%E4%BD%93/04%20-%20LC-2812%20-%20Find%20the%20Safest%20Path%20in%20a%20Grid) | M | maximin：先多源 BFS 算安全度，再 `relax = min(d, safe)`，大根堆 |

### 03 - Dijkstra 最短路计数与结果组合

距离本身用标准模板算，考点在**算完之后怎么加工**：顺带计数、跑多次、跑反图。

| | 题号 | 题目 | 难度 | 主要考点 |
|---|---|---|---|---|
| ★ | LC-1976 | [LC-1976 - Number of Ways to Arrive at Destination](03%20-%20Dijkstra%20%E6%9C%80%E7%9F%AD%E8%B7%AF%E8%AE%A1%E6%95%B0%E4%B8%8E%E7%BB%93%E6%9E%9C%E7%BB%84%E5%90%88/01%20-%20LC-1976%20-%20Number%20of%20Ways%20to%20Arrive%20at%20Destination) | M | dist 和 ways 同时维护：严格更短时重置、相等时累加 |
| ○ | LC-3123 | [LC-3123 - Find Edges in Shortest Paths](03%20-%20Dijkstra%20%E6%9C%80%E7%9F%AD%E8%B7%AF%E8%AE%A1%E6%95%B0%E4%B8%8E%E7%BB%93%E6%9E%9C%E7%BB%84%E5%90%88/02%20-%20LC-3123%20-%20Find%20Edges%20in%20Shortest%20Paths) | H | 正反各跑一次，判 `d0[u] + w + d1[v] == D` |
| ○ | LC-2203 | [LC-2203 - Minimum Weighted Subgraph With the Required Paths](03%20-%20Dijkstra%20%E6%9C%80%E7%9F%AD%E8%B7%AF%E8%AE%A1%E6%95%B0%E4%B8%8E%E7%BB%93%E6%9E%9C%E7%BB%84%E5%90%88/03%20-%20LC-2203%20-%20Minimum%20Weighted%20Subgraph%20With%20the%20Required%20Paths) | H | 两个起点各跑一次 + 反图从终点跑一次，枚举汇合点 |
| ★ | LC-1786 | [LC-1786 - Number of Restricted Paths From First to Last Node](03%20-%20Dijkstra%20%E6%9C%80%E7%9F%AD%E8%B7%AF%E8%AE%A1%E6%95%B0%E4%B8%8E%E7%BB%93%E6%9E%9C%E7%BB%84%E5%90%88/04%20-%20LC-1786%20-%20Number%20of%20Restricted%20Paths%20From%20First%20to%20Last%20Node) | M | 反向 Dijkstra 定方向 + DAG 上计数；3123 和 1976 的合体 |

### 04 - Dijkstra 网格建图与特殊边权

点是格子、边是四方向，**不用先建邻接表**。边权特殊（0/1、滚动距离）但 relax 仍是 `d + w`。

| | 题号 | 题目 | 难度 | 主要考点 |
|---|---|---|---|---|
| ★ | LC-2290 | [LC-2290 - Minimum Obstacle Removal to Reach Corner](<../zero-one-bfs (0-1 BFS：双端队列，0 放队头 1 放队尾)/LC-2290 - Minimum Obstacle Removal to Reach Corner>) | H | 0/1 权网格；标准 Dijkstra 可解，0-1 BFS 更快 |
| ○ | LC-1368 | [LC-1368 - Minimum Cost to Make at Least One Valid Path in a Grid](<../zero-one-bfs (0-1 BFS：双端队列，0 放队头 1 放队尾)/LC-1368 - Minimum Cost to Make at Least One Valid Path in a Grid>) | H | 方向决定 0/1 权；代价记在**离开**的格子上 |
| ○ | LC-0505 | [LC-0505 - The Maze II](<04 - Dijkstra 网格建图与特殊边权/01 - LC-0505 - The Maze II>) | M | 一路滚到撞墙才算一次转移，边权 = 滚动距离 |

### 05 - Dijkstra 状态扩展与时间约束

`dist[node]` 不够用了：存在额外的资源维度或时间约束，必须扩状态，或者换 Bellman-Ford。

| | 题号 | 题目 | 难度 | 主要考点 |
|---|---|---|---|---|
| ★ | LC-0787 | [LC-0787 - Cheapest Flights Within K Stops](<../bellman-ford (Bellman-Ford：限制 k 条边，每轮用快照)/LC-0787 - Cheapest Flights Within K Stops - ★ 签名题>) | M | 状态 = (node, 已用航段)；**Bellman-Ford + 快照更简单更快** |
| ○ | LC-1928 | [LC-1928 - Minimum Cost to Reach Destination in Time](<05 - Dijkstra 状态扩展与时间约束/01 - LC-1928 - Minimum Cost to Reach Destination in Time>) | H | 状态 = (node, 已花时间)，在时间约束下最小化费用 |
| ○ | LC-2577 | [LC-2577 - Minimum Time to Visit a Cell In a Grid](<05 - Dijkstra 状态扩展与时间约束/02 - LC-2577 - Minimum Time to Visit a Cell In a Grid>) | H | 时间依赖转移：等待可行性 + 奇偶性，不是多维 dist |

## Standard Dijkstra 与 Dijkstra Variants 的最小区别

| 题 | 和签名题 743 比，改了哪一行 |
|---|---|
| 1334 / 2642 / 2976 | **一行都没改**，难点在建模和调用次数 |
| 1631 | `nd = d + w` → `nd = max(d, w)` |
| 0778 | `nd = d + w` → `nd = max(d, grid[nr][nc])`（权在点上不在边上）|
| 1514 | `nd = d + w` → `nd = d * w`，并把堆里的键取负变成大根堆 |
| 2812 | `nd = d + w` → `nd = min(d, safe[nr][nc])`，大根堆，外加一次多源 BFS 预处理 |
| 1976 | 模板不变，`dist[v] > nd` 时 `ways[v] = ways[u]`，`== nd` 时 `ways[v] += ways[u]` |
| 3123 | 模板不变，跑两次（起点一次、终点一次），再 O(E) 判边 |
| 2203 | 模板不变，跑三次（两个起点 + 反图上的终点），枚举汇合点 |
| 1786 | 模板不变，**从终点跑**，再把 `dist[u] > dist[v]` 当作边的方向，在这张 DAG 上递推计数 |
| 2290 / 1368 | 模板不变，边权只有 0/1；邻接表换成四方向隐式建图 |
| 0505 | 模板不变，「一次转移」从「走一格」变成「滚到撞墙」 |
| 0787 / 1928 | `dist[node]` → `dist[node][资源]`，堆里多存一维 |
| 2577 | 模板不变，relax 里插一个「什么时候才允许进这格」的时间判断 |

## 什么时候需要状态扩展（state expansion）

判断方法只有一句话：**把「到 u 的最优值」定下来之后，后面的决策是不是只跟 u 有关？**

- 是 → 标准 `dist[node]` 够用。

- 否（还取决于「我是怎么来的」：用了几条边、花了多少时间、还剩几次免费机会）→ 把那一维加进状态，变成 `dist[node][资源]`，堆里一起存。


典型信号词：**最多 k 次 / 限时 / 还剩几次机会 / 必须恰好**。

反例要特别小心 **2577**：它看起来像状态扩展，其实时间是**被距离唯一决定**的，只要在 relax 里判断「能不能进」（必要时靠来回走两步等奇偶性），`dist[node]` 就够了。

## Dijkstra / Bellman-Ford / 0-1 BFS 怎么选

| | 适用条件 | 复杂度 | 这套题里什么时候用 |
|---|---|---|---|
| **Dijkstra**（堆） | 代价函数单调（非负权是最常见的特例）| `O(E log V)` | 默认选它，18 题里 16 题的主解法 |
| **Bellman-Ford**（+ 快照 snapshot）| 有负权，或**限制边数 k** | `O(k * E)` | 787 的首选；1928 也可以写 |
| **0-1 BFS**（双端队列 deque）| 边权只有 0 和 1 | `O(V + E)` | 2290、1368 的最优解；0 放队头、1 放队尾 |

Bellman-Ford 的「快照」是它在 787 这类题上胜过 Dijkstra 的原因：**第 i 轮结束时 `dist[v]` 恰好等于「最多用 i 条边到 v 的最小花费」**，轮数天然就是边数，不用自己扩状态。前提是每轮必须基于上一轮的拷贝松弛，直接原地改会一轮串起好几条边。

0-1 BFS 值得知道、不值得为它专门背模板：面试里先给 Dijkstra 版本，再用一句话说明「边权只有 0/1，可以用双端队列省掉 log」，加分已经拿到了。

## 不用背的

- **SPFA**：最坏退化成 `O(V*E)`，竞赛里早被卡，面试不要提。要负权就说 Bellman-Ford。

- **Floyd-Warshall**：只在点数极小时（1334 的 `n <= 100`、2976 的 26 个字母）顺手写三重循环，知道「k 必须在最外层」就够了，不作为独立模板记忆。

- **Johnson、A\***、**最小树形图**：这套题一个都用不上。

## 推荐刷题顺序

先把骨架打通，再补变体，最后才碰状态扩展：

```
743 → 1334 → 1631 → 778 → 1514 → 2290 → 1368 → 787 → 1976 → 3123 → 1786 → 2642 → 2976 → 505 → 2812 → 2203 → 1928 → 2577
```

| 阶段 | 题 | 目标 |
|---|---|---|
| 打地基 | 743 → 1334 | 模板能闭卷默写，包括作废票那一行 |
| 换 relax | 1631 → 778 → 1514 | 明白「只改一行」到底改的是什么，能当场推单调性 |
| 网格建图 | 2290 → 1368 | 不建邻接表直接在网格上跑；顺带点出 0-1 BFS |
| 加维度 | 787 | 第一次遇到 `dist[node]` 不够用，同时学会 Bellman-Ford 快照 |
| 加工结果 | 1976 → 3123 → 1786 → 2642 → 2976 | 计数、判边、反图定向、多次调用、建模 |
| 收尾 | 505 → 2812 → 2203 → 1928 → 2577 | 偏难，能讲清思路即可 |

## 共享资料

`_resources/`：`dijkstra 的本质.png`、`minimax_maximin.jpg`、`00 - Dijkstra Explanation - William Fiset.mp4`。

