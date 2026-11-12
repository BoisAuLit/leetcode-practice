# 06-mst (阶段 5 · 最小生成树与 Kruskal 过程)

**目标**：Kruskal、Prim 数组版、Prim 堆版三套模板，以及"Kruskal 过程不要树"的用法。

**出关标准**：1584 三种写法、1697 离线写法盲写；能讲清 1489 的两个实验。

标记：★ 签名题（每个模板只绑一道，进复习系统时优先盲写）· ○ 核心变体 · △ 扩展。
每道题只问一句：**和签名题比改了哪一行？**

## [第 1 层: 伪装成别的故事的 MST(建模题)](%E7%AC%AC%201%20%E5%B1%82%3A%20%E4%BC%AA%E8%A3%85%E6%88%90%E5%88%AB%E7%9A%84%E6%95%85%E4%BA%8B%E7%9A%84%20MST%28%E5%BB%BA%E6%A8%A1%E9%A2%98%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 1584 Min Cost to Connect All Points](%E7%AC%AC%201%20%E5%B1%82%3A%20%E4%BC%AA%E8%A3%85%E6%88%90%E5%88%AB%E7%9A%84%E6%95%85%E4%BA%8B%E7%9A%84%20MST%28%E5%BB%BA%E6%A8%A1%E9%A2%98%29/LC-1584%20-%20Min%20Cost%20to%20Connect%20All%20Points%20-%20%E7%BA%AF%E7%B2%B9%E7%9A%84%20MST%20-%20%E7%A8%A0%E5%AF%86%E5%9B%BE%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 坐标点连通最小曼哈顿总长 | MST 签名题，完全图用 Prim 数组版 |
| ○ | [LC 1135 Connecting Cities With Minimum Cost](%E7%AC%AC%201%20%E5%B1%82%3A%20%E4%BC%AA%E8%A3%85%E6%88%90%E5%88%AB%E7%9A%84%E6%95%85%E4%BA%8B%E7%9A%84%20MST%28%E5%BB%BA%E6%A8%A1%E9%A2%98%29/LC-1135%20-%20Connecting%20Cities%20With%20Min%20Cost%20-%20%E7%A8%80%E7%96%8F%E5%9B%BE) | 边列表、可能不连通（会员） | Kruskal / Prim 堆版 |
| ○ | [LC 1168 Optimize Water Distribution in a Village](%E7%AC%AC%201%20%E5%B1%82%3A%20%E4%BC%AA%E8%A3%85%E6%88%90%E5%88%AB%E7%9A%84%E6%95%85%E4%BA%8B%E7%9A%84%20MST%28%E5%BB%BA%E6%A8%A1%E9%A2%98%29/LC-1168%20-%20Optimize%20Water%20Distribution%20in%20a%20Village%20-%20%E8%99%9A%E6%8B%9F%E6%BA%90%E7%82%B9%20-%20%E7%A8%80%E7%96%8F%E5%9B%BE) | 打井或接水管（会员） | 虚拟源点建模 |

## [第 2 层: 追问 MST 结构 (只能用 Kruskal 做)](%E7%AC%AC%202%20%E5%B1%82%3A%20%E8%BF%BD%E9%97%AE%20MST%20%E7%BB%93%E6%9E%84%20%28%E5%8F%AA%E8%83%BD%E7%94%A8%20Kruskal%20%E5%81%9A%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ○ | [LC 1489 Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree](%E7%AC%AC%202%20%E5%B1%82%3A%20%E8%BF%BD%E9%97%AE%20MST%20%E7%BB%93%E6%9E%84%20%28%E5%8F%AA%E8%83%BD%E7%94%A8%20Kruskal%20%E5%81%9A%29/LC-1489%20-%20Critical%20%26%20Pseudo%20Critical%20Edges%20in%20MST) | 哪些边必须在 MST 里、哪些可有可无 | 排除实验 + 强制实验 |
| ○ | [LC 1579 Remove Max Number of Edges to Keep Graph Fully Traversable](%E7%AC%AC%202%20%E5%B1%82%3A%20%E8%BF%BD%E9%97%AE%20MST%20%E7%BB%93%E6%9E%84%20%28%E5%8F%AA%E8%83%BD%E7%94%A8%20Kruskal%20%E5%81%9A%29/LC-1579%20-%20Remove%20Max%20Number%20of%20Edges%20to%20Keep%20Graph%20Fully%20Traversable) | Alice/Bob 各能走的边，最多删几条 | 两个并查集，公共边优先 |

## [第 3 层: 瓶颈路径与阈值连通 (用 Kruskal 的过程, 不要树)](%E7%AC%AC%203%20%E5%B1%82%3A%20%E7%93%B6%E9%A2%88%E8%B7%AF%E5%BE%84%E4%B8%8E%E9%98%88%E5%80%BC%E8%BF%9E%E9%80%9A%20%28%E7%94%A8%20Kruskal%20%E7%9A%84%E8%BF%87%E7%A8%8B%2C%20%E4%B8%8D%E8%A6%81%E6%A0%91%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 1697 Checking Existence of Edge Length Limited Paths](%E7%AC%AC%203%20%E5%B1%82%3A%20%E7%93%B6%E9%A2%88%E8%B7%AF%E5%BE%84%E4%B8%8E%E9%98%88%E5%80%BC%E8%BF%9E%E9%80%9A%20%28%E7%94%A8%20Kruskal%20%E7%9A%84%E8%BF%87%E7%A8%8B%2C%20%E4%B8%8D%E8%A6%81%E6%A0%91%29/LC-1697%20-%20Checking%20Existence%20of%20Edge%20Length%20Limited%20Paths%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 多组"只用 < limit 的边 p、q 通不通" | 离线 + Kruskal 过程签名题 |
| ○ | [LC 1970 Last Day Where You Can Still Cross](%E7%AC%AC%203%20%E5%B1%82%3A%20%E7%93%B6%E9%A2%88%E8%B7%AF%E5%BE%84%E4%B8%8E%E9%98%88%E5%80%BC%E8%BF%9E%E9%80%9A%20%28%E7%94%A8%20Kruskal%20%E7%9A%84%E8%BF%87%E7%A8%8B%2C%20%E4%B8%8D%E8%A6%81%E6%A0%91%29/LC-1970%20-%20Last%20Day%20Where%20You%20Can%20Still%20Cross) | 格子逐天被淹，最后哪天能上下穿越 | 时间倒放 + 并查集 + 虚拟顶/底点 |
| ○ | [LC 2421 Number of Good Paths](%E7%AC%AC%203%20%E5%B1%82%3A%20%E7%93%B6%E9%A2%88%E8%B7%AF%E5%BE%84%E4%B8%8E%E9%98%88%E5%80%BC%E8%BF%9E%E9%80%9A%20%28%E7%94%A8%20Kruskal%20%E7%9A%84%E8%BF%87%E7%A8%8B%2C%20%E4%B8%8D%E8%A6%81%E6%A0%91%29/LC-2421%20-%20Number%20of%20Good%20Paths) | 树上起终点同值、中间不大于的路径数 | 点按值升序加入，每派数同值点 |
| △ | [LC 1724 Checking Existence of Edge Length Limited Paths II](%E7%AC%AC%203%20%E5%B1%82%3A%20%E7%93%B6%E9%A2%88%E8%B7%AF%E5%BE%84%E4%B8%8E%E9%98%88%E5%80%BC%E8%BF%9E%E9%80%9A%20%28%E7%94%A8%20Kruskal%20%E7%9A%84%E8%BF%87%E7%A8%8B%2C%20%E4%B8%8D%E8%A6%81%E6%A0%91%29/LC-1724%20-%20Checking%20Existence%20of%20Edge%20Length%20Limited%20Paths%20II) | 1697 的在线版（会员） | Kruskal 重构树 / 不压缩路径的并查集按权跳，了解即可 |

## 另外两层：题不在这里

手册把 MST 分五层。第 1-3 层在上面；第 4、5 层各有一个文件夹，里面只有说明：

- **[第 4 层: 单源瓶颈路径 (Prim 或 Dijkstra 的骨架改 relax)](%E7%AC%AC%204%20%E5%B1%82%3A%20%E5%8D%95%E6%BA%90%E7%93%B6%E9%A2%88%E8%B7%AF%E5%BE%84%20%28Prim%20%E6%88%96%20Dijkstra%20%E7%9A%84%E9%AA%A8%E6%9E%B6%E6%94%B9%20relax%29)**：和第 3 层是同一批题（1631、778、1102）的另一种解法，所以题目放在阶段 4 的 `bottleneck-path`，一道题只留一个文件夹（否则复习队列会重复抽）。那三个 `solution.py` 里两层的解法都写了。
- **[第 5 层: LeetCode 之外的真实用途 (聚类、近似算法、迷宫)](%E7%AC%AC%205%20%E5%B1%82%3A%20LeetCode%20%E4%B9%8B%E5%A4%96%E7%9A%84%E7%9C%9F%E5%AE%9E%E7%94%A8%E9%80%94%20%28%E8%81%9A%E7%B1%BB%E3%80%81%E8%BF%91%E4%BC%BC%E7%AE%97%E6%B3%95%E3%80%81%E8%BF%B7%E5%AE%AB%29)**：没有 LeetCode 题，不进复习队列；单链接聚类、TSP 2 倍近似、随机迷宫三个用途有可运行的 demo。

---

每题文件夹：`solution.py`（所有解法 + 复杂度 + ⭐ 最优）、`problem.pdf` / `problem_dark.pdf`、`metadata.json`（复习记录）。
模板在 [00-foundations/templates (模板)](../00-foundations%20%28%E5%9B%BE%E8%AE%BA%E5%9F%BA%E7%A1%80%E3%80%81%E5%9B%BE%E8%AE%BA%E6%89%8B%E5%86%8C%29/templates%20%28%E6%A8%A1%E6%9D%BF%29)，总表在 [../README.md](../README.md)。
