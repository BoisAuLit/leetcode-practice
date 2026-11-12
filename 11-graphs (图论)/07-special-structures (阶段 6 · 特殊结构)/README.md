# 07-special-structures (阶段 6 · 特殊结构)

**目标**：二分图染色会写；Tarjan 求桥会写一版；欧拉路径和 SCC 知道思路。

**出关标准**：785、1192 能写；332 能讲 Hierholzer 的"后序入栈再反转"。

标记：★ 签名题（每个模板只绑一道，进复习系统时优先盲写）· ○ 核心变体 · △ 扩展。
每道题只问一句：**和签名题比改了哪一行？**

## [bipartite (二分图染色)](bipartite%20%28%E4%BA%8C%E5%88%86%E5%9B%BE%E6%9F%93%E8%89%B2%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 785 Is Graph Bipartite?](bipartite%20%28%E4%BA%8C%E5%88%86%E5%9B%BE%E6%9F%93%E8%89%B2%29/LC-0785%20-%20Is%20Graph%20Bipartite%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 能否分成两组使每条边跨组 | BFS/DFS 二染色签名题，相邻同色即失败 |
| ○ | [LC 886 Possible Bipartition](bipartite%20%28%E4%BA%8C%E5%88%86%E5%9B%BE%E6%9F%93%E8%89%B2%29/LC-0886%20-%20Possible%20Bipartition) | 有矛盾的人不能同组，能否分两组 | 785 换个故事 |

## [tarjan-bridges (Tarjan 求桥、割点)](tarjan-bridges%20%28Tarjan%20%E6%B1%82%E6%A1%A5%E3%80%81%E5%89%B2%E7%82%B9%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 1192 Critical Connections in a Network](tarjan-bridges%20%28Tarjan%20%E6%B1%82%E6%A1%A5%E3%80%81%E5%89%B2%E7%82%B9%29/LC-1192%20-%20Critical%20Connections%20in%20a%20Network%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 删掉哪条边会让网络断开 | Tarjan 求桥签名题，low[v] > disc[u] |
| △ | [LC 1568 Minimum Number of Days to Disconnect Island](tarjan-bridges%20%28Tarjan%20%E6%B1%82%E6%A1%A5%E3%80%81%E5%89%B2%E7%82%B9%29/LC-1568%20-%20Minimum%20Number%20of%20Days%20to%20Disconnect%20Island) | 最少去掉几格让岛不连通 | 答案只能是 0/1/2，枚举去掉一格，本质是割点 |

## [eulerian-path (欧拉路径 Hierholzer)](eulerian-path%20%28%E6%AC%A7%E6%8B%89%E8%B7%AF%E5%BE%84%20Hierholzer%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ○ | [LC 332 Reconstruct Itinerary](eulerian-path%20%28%E6%AC%A7%E6%8B%89%E8%B7%AF%E5%BE%84%20Hierholzer%29/LC-0332%20-%20Reconstruct%20Itinerary) | 用完所有机票的字典序最小行程 | Hierholzer 欧拉路径，后序入栈再反转 |
| △ | [LC 2097 Valid Arrangement of Pairs](eulerian-path%20%28%E6%AC%A7%E6%8B%89%E8%B7%AF%E5%BE%84%20Hierholzer%29/LC-2097%20-%20Valid%20Arrangement%20of%20Pairs) | 把数对首尾相接排成一列 | 欧拉路径，起点是出度比入度多 1 的点 |

## [tree-problems (树上问题：直径、换根 DP)](tree-problems%20%28%E6%A0%91%E4%B8%8A%E9%97%AE%E9%A2%98%EF%BC%9A%E7%9B%B4%E5%BE%84%E3%80%81%E6%8D%A2%E6%A0%B9%20DP%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ○ | [LC 1245 Tree Diameter](tree-problems%20%28%E6%A0%91%E4%B8%8A%E9%97%AE%E9%A2%98%EF%BC%9A%E7%9B%B4%E5%BE%84%E3%80%81%E6%8D%A2%E6%A0%B9%20DP%29/LC-1245%20-%20Tree%20Diameter) | 树上最远两点距离（会员） | 两次 BFS/DFS：任意点出发找最远点 a，再从 a 出发找最远点 |
| △ | [LC 834 Sum of Distances in Tree](tree-problems%20%28%E6%A0%91%E4%B8%8A%E9%97%AE%E9%A2%98%EF%BC%9A%E7%9B%B4%E5%BE%84%E3%80%81%E6%8D%A2%E6%A0%B9%20DP%29/LC-0834%20-%20Sum%20of%20Distances%20in%20Tree) | 每个点到其他所有点的距离和 | 换根 DP，树形 DP 的代表 |

---

每题文件夹：`solution.py`（所有解法 + 复杂度 + ⭐ 最优）、`problem.pdf` / `problem_dark.pdf`、`metadata.json`（复习记录）。
模板在 [00-foundations/templates (模板)](../00-foundations%20%28%E5%9B%BE%E8%AE%BA%E5%9F%BA%E7%A1%80%E3%80%81%E5%9B%BE%E8%AE%BA%E6%89%8B%E5%86%8C%29/templates%20%28%E6%A8%A1%E6%9D%BF%29)，总表在 [../README.md](../README.md)。
