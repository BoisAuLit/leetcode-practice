# 02-dfs-bfs (阶段 1 · DFS、BFS：静态无权的连通性与步数)

**目标**：洪水填充、多源 BFS、边界反向 DFS 三个套路写到不用想。

**出关标准**：200、994、417 三题各 10 分钟内盲写。

标记：★ 签名题（每个模板只绑一道，进复习系统时优先盲写）· ○ 核心变体 · △ 扩展。
每道题只问一句：**和签名题比改了哪一行？**

## [flood-fill (洪水填充：数连通块)](flood-fill%20%28%E6%B4%AA%E6%B0%B4%E5%A1%AB%E5%85%85%EF%BC%9A%E6%95%B0%E8%BF%9E%E9%80%9A%E5%9D%97%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 200 Number of Islands](flood-fill%20%28%E6%B4%AA%E6%B0%B4%E5%A1%AB%E5%85%85%EF%BC%9A%E6%95%B0%E8%BF%9E%E9%80%9A%E5%9D%97%29/LC-0200%20-%20Number%20of%20Islands%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 静态网格数岛 | DFS 洪水填充签名题 |
| ○ | [LC 695 Max Area of Island](flood-fill%20%28%E6%B4%AA%E6%B0%B4%E5%A1%AB%E5%85%85%EF%BC%9A%E6%95%B0%E8%BF%9E%E9%80%9A%E5%9D%97%29/LC-0695%20-%20Max%20Area%20of%20Island) | 最大的岛有几格 | DFS 返回面积，改一行 |
| ○ | [LC 547 Number of Provinces](flood-fill%20%28%E6%B4%AA%E6%B0%B4%E5%A1%AB%E5%85%85%EF%BC%9A%E6%95%B0%E8%BF%9E%E9%80%9A%E5%9D%97%29/LC-0547%20-%20Number%20of%20Provinces) | 邻接矩阵表示的朋友圈有几个 | DFS 数连通块（也可并查集），和 200 的区别只是图的存法 |

## [boundary-first (边界优先：从边界反向 DFS)](boundary-first%20%28%E8%BE%B9%E7%95%8C%E4%BC%98%E5%85%88%EF%BC%9A%E4%BB%8E%E8%BE%B9%E7%95%8C%E5%8F%8D%E5%90%91%20DFS%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 417 Pacific Atlantic Water Flow](boundary-first%20%28%E8%BE%B9%E7%95%8C%E4%BC%98%E5%85%88%EF%BC%9A%E4%BB%8E%E8%BE%B9%E7%95%8C%E5%8F%8D%E5%90%91%20DFS%29/LC-0417%20-%20Pacific%20Atlantic%20Water%20Flow%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 哪些格子的水既能流到太平洋又能流到大西洋 | 边界反向 DFS 签名题：从两边海岸往高处爬，取交集 |
| ○ | [LC 130 Surrounded Regions](boundary-first%20%28%E8%BE%B9%E7%95%8C%E4%BC%98%E5%85%88%EF%BC%9A%E4%BB%8E%E8%BE%B9%E7%95%8C%E5%8F%8D%E5%90%91%20DFS%29/LC-0130%20-%20Surrounded%20Regions) | 被 X 包围的 O 改成 X | 从边界 O 反向标记 |
| ○ | [LC 1254 Number of Closed Islands](boundary-first%20%28%E8%BE%B9%E7%95%8C%E4%BC%98%E5%85%88%EF%BC%9A%E4%BB%8E%E8%BE%B9%E7%95%8C%E5%8F%8D%E5%90%91%20DFS%29/LC-1254%20-%20Number%20of%20Closed%20Islands) | 不碰边界的岛有几个 | 先把边界相连的淹掉再数，"边界优先"套路 |
| ○ | [LC 1020 Number of Enclaves](boundary-first%20%28%E8%BE%B9%E7%95%8C%E4%BC%98%E5%85%88%EF%BC%9A%E4%BB%8E%E8%BE%B9%E7%95%8C%E5%8F%8D%E5%90%91%20DFS%29/LC-1020%20-%20Number%20of%20Enclaves) | 走不出边界的陆地格有几个 | 同 1254，数格子而不是数岛 |

## [multi-source-bfs (多源 BFS：所有起点一起入队)](multi-source-bfs%20%28%E5%A4%9A%E6%BA%90%20BFS%EF%BC%9A%E6%89%80%E6%9C%89%E8%B5%B7%E7%82%B9%E4%B8%80%E8%B5%B7%E5%85%A5%E9%98%9F%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 994 Rotting Oranges](multi-source-bfs%20%28%E5%A4%9A%E6%BA%90%20BFS%EF%BC%9A%E6%89%80%E6%9C%89%E8%B5%B7%E7%82%B9%E4%B8%80%E8%B5%B7%E5%85%A5%E9%98%9F%29/LC-0994%20-%20Rotting%20Oranges%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 腐烂传播到全部需要几分钟 | 多源 BFS 签名题：所有烂橘子一起进队列 |
| ○ | [LC 542 01 Matrix](multi-source-bfs%20%28%E5%A4%9A%E6%BA%90%20BFS%EF%BC%9A%E6%89%80%E6%9C%89%E8%B5%B7%E7%82%B9%E4%B8%80%E8%B5%B7%E5%85%A5%E9%98%9F%29/LC-0542%20-%2001%20Matrix) | 每个格子到最近 0 的距离 | 多源 BFS，所有 0 一起出发 |
| ○ | [LC 286 Walls and Gates](multi-source-bfs%20%28%E5%A4%9A%E6%BA%90%20BFS%EF%BC%9A%E6%89%80%E6%9C%89%E8%B5%B7%E7%82%B9%E4%B8%80%E8%B5%B7%E5%85%A5%E9%98%9F%29/LC-0286%20-%20Walls%20and%20Gates) | 每个空房间到最近门的距离（会员） | 同 542 |
| ○ | [LC 1162 As Far from Land as Possible](multi-source-bfs%20%28%E5%A4%9A%E6%BA%90%20BFS%EF%BC%9A%E6%89%80%E6%9C%89%E8%B5%B7%E7%82%B9%E4%B8%80%E8%B5%B7%E5%85%A5%E9%98%9F%29/LC-1162%20-%20As%20Far%20from%20Land%20as%20Possible) | 离陆地最远的海洋格有多远 | 多源 BFS 的最后一层 |
| ○ | [LC 317 Shortest Distance from All Buildings](multi-source-bfs%20%28%E5%A4%9A%E6%BA%90%20BFS%EF%BC%9A%E6%89%80%E6%9C%89%E8%B5%B7%E7%82%B9%E4%B8%80%E8%B5%B7%E5%85%A5%E9%98%9F%29/LC-0317%20-%20Shortest%20Distance%20from%20All%20Buildings) | 找一块空地，到所有楼的距离和最小（会员） | 从每栋楼各做一次 BFS 累加距离；只扩展所有楼都能到的格子 |
| ○ | [LC 934 Shortest Bridge](multi-source-bfs%20%28%E5%A4%9A%E6%BA%90%20BFS%EF%BC%9A%E6%89%80%E6%9C%89%E8%B5%B7%E7%82%B9%E4%B8%80%E8%B5%B7%E5%85%A5%E9%98%9F%29/LC-0934%20-%20Shortest%20Bridge) | 两座岛之间最少填几格海 | 先 DFS 把第一座岛全部入队，再多源 BFS 扩张碰到第二座岛 |

## [bfs-steps (BFS 层数 = 步数)](bfs-steps%20%28BFS%20%E5%B1%82%E6%95%B0%20%3D%20%E6%AD%A5%E6%95%B0%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ○ | [LC 1091 Shortest Path in Binary Matrix](bfs-steps%20%28BFS%20%E5%B1%82%E6%95%B0%20%3D%20%E6%AD%A5%E6%95%B0%29/LC-1091%20-%20Shortest%20Path%20in%20Binary%20Matrix) | 八方向网格最短路 | BFS 按层计数，练"层数 = 步数" |
| ○ | [LC 1926 Nearest Exit from Entrance in Maze](bfs-steps%20%28BFS%20%E5%B1%82%E6%95%B0%20%3D%20%E6%AD%A5%E6%95%B0%29/LC-1926%20-%20Nearest%20Exit%20from%20Entrance%20in%20Maze) | 从入口到最近出口几步 | BFS，注意入口本身不算出口 |
| △ | [LC 1197 Minimum Knight Moves](bfs-steps%20%28BFS%20%E5%B1%82%E6%95%B0%20%3D%20%E6%AD%A5%E6%95%B0%29/LC-1197%20-%20Minimum%20Knight%20Moves) | 无限棋盘马走到目标最少几步（会员） | BFS + 对称剪枝 |

## [weighted-dfs (带权图上的 DFS：累乘、带权深度，不求最短路)](weighted-dfs%20%28%E5%B8%A6%E6%9D%83%E5%9B%BE%E4%B8%8A%E7%9A%84%20DFS%EF%BC%9A%E7%B4%AF%E4%B9%98%E3%80%81%E5%B8%A6%E6%9D%83%E6%B7%B1%E5%BA%A6%EF%BC%8C%E4%B8%8D%E6%B1%82%E6%9C%80%E7%9F%AD%E8%B7%AF%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ○ | [LC 399 Evaluate Division](weighted-dfs%20%28%E5%B8%A6%E6%9D%83%E5%9B%BE%E4%B8%8A%E7%9A%84%20DFS%EF%BC%9A%E7%B4%AF%E4%B9%98%E3%80%81%E5%B8%A6%E6%9D%83%E6%B7%B1%E5%BA%A6%EF%BC%8C%E4%B8%8D%E6%B1%82%E6%9C%80%E7%9F%AD%E8%B7%AF%29/LC-0399%20-%20Evaluate%20Division) | 给 a/b = 2、b/c = 3，问 a/c | 带权有向图上 DFS 累乘路径权重，"图可以有权但不需要最短路"的例子 |
| ○ | [LC 1376 Time Needed to Inform All Employees](weighted-dfs%20%28%E5%B8%A6%E6%9D%83%E5%9B%BE%E4%B8%8A%E7%9A%84%20DFS%EF%BC%9A%E7%B4%AF%E4%B9%98%E3%80%81%E5%B8%A6%E6%9D%83%E6%B7%B1%E5%BA%A6%EF%BC%8C%E4%B8%8D%E6%B1%82%E6%9C%80%E7%9F%AD%E8%B7%AF%29/LC-1376%20-%20Time%20Needed%20to%20Inform%20All%20Employees) | 消息从 CEO 传到所有人要多久 | 树上 DFS 求带权深度最大值 |
| △ | [LC 2101 Detonate the Maximum Bombs](weighted-dfs%20%28%E5%B8%A6%E6%9D%83%E5%9B%BE%E4%B8%8A%E7%9A%84%20DFS%EF%BC%9A%E7%B4%AF%E4%B9%98%E3%80%81%E5%B8%A6%E6%9D%83%E6%B7%B1%E5%BA%A6%EF%BC%8C%E4%B8%8D%E6%B1%82%E6%9C%80%E7%9F%AD%E8%B7%AF%29/LC-2101%20-%20Detonate%20the%20Maximum%20Bombs) | 引爆一个炸弹最多连锁多少个 | 先按距离建有向图，再从每个点 DFS 取最大 |

## [functional-graph (函数图：每个点只有一条出边)](functional-graph%20%28%E5%87%BD%E6%95%B0%E5%9B%BE%EF%BC%9A%E6%AF%8F%E4%B8%AA%E7%82%B9%E5%8F%AA%E6%9C%89%E4%B8%80%E6%9D%A1%E5%87%BA%E8%BE%B9%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| △ | [LC 2359 Find Closest Node to Given Two Nodes](functional-graph%20%28%E5%87%BD%E6%95%B0%E5%9B%BE%EF%BC%9A%E6%AF%8F%E4%B8%AA%E7%82%B9%E5%8F%AA%E6%9C%89%E4%B8%80%E6%9D%A1%E5%87%BA%E8%BE%B9%29/LC-2359%20-%20Find%20Closest%20Node%20to%20Given%20Two%20Nodes) | 每个点只有一条出边，离两个起点都最近的点 | 沿唯一出边走并记录距离 |
| △ | [LC 2360 Longest Cycle in a Graph](functional-graph%20%28%E5%87%BD%E6%95%B0%E5%9B%BE%EF%BC%9A%E6%AF%8F%E4%B8%AA%E7%82%B9%E5%8F%AA%E6%9C%89%E4%B8%80%E6%9D%A1%E5%87%BA%E8%BE%B9%29/LC-2360%20-%20Longest%20Cycle%20in%20a%20Graph) | 每个点只有一条出边，最长的环多长 | 沿着唯一出边走并记录时间戳，是一类特殊的 DFS |

## [nested-dfs (嵌套结构上的 DFS)](nested-dfs%20%28%E5%B5%8C%E5%A5%97%E7%BB%93%E6%9E%84%E4%B8%8A%E7%9A%84%20DFS%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ○ | [LC 339 Nested List Weight Sum](nested-dfs%20%28%E5%B5%8C%E5%A5%97%E7%BB%93%E6%9E%84%E4%B8%8A%E7%9A%84%20DFS%29/LC-0339%20-%20Nested%20List%20Weight%20Sum) | 嵌套列表按深度加权求和（会员） | DFS 把 depth 往下传；不是图题，但就是同一个递归动作 |
| ○ | [LC 364 Nested List Weight Sum II](nested-dfs%20%28%E5%B5%8C%E5%A5%97%E7%BB%93%E6%9E%84%E4%B8%8A%E7%9A%84%20DFS%29/LC-0364%20-%20Nested%20List%20Weight%20Sum%20II) | 权重反过来：越浅权重越大（会员） | 先求最大深度再 DFS，或 BFS 用"前缀累加"一遍过 |

---

每题文件夹：`solution.py`（所有解法 + 复杂度 + ⭐ 最优）、`problem.pdf` / `problem_dark.pdf`、`metadata.json`（复习记录）。
模板在 [00-foundations/templates (模板)](../00-foundations%20%28%E5%9B%BE%E8%AE%BA%E5%9F%BA%E7%A1%80%E3%80%81%E5%9B%BE%E8%AE%BA%E6%89%8B%E5%86%8C%29/templates%20%28%E6%A8%A1%E6%9D%BF%29)，总表在 [../README.md](../README.md)。
