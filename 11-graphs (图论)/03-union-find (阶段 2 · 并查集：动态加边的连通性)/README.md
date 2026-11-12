# 03-union-find (阶段 2 · 并查集：动态加边的连通性)

**目标**：并查集模板闭眼写；分清"静态用 DFS、动态用并查集"。

**出关标准**：323、684、305 盲写，并能解释 union 返回值的用途。

标记：★ 签名题（每个模板只绑一道，进复习系统时优先盲写）· ○ 核心变体 · △ 扩展。
每道题只问一句：**和签名题比改了哪一行？**

## [count-components (计数：块数 = n − 成功合并次数)](count-components%20%28%E8%AE%A1%E6%95%B0%EF%BC%9A%E5%9D%97%E6%95%B0%20%3D%20n%20%E2%88%92%20%E6%88%90%E5%8A%9F%E5%90%88%E5%B9%B6%E6%AC%A1%E6%95%B0%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 323 Number of Connected Components in an Undirected Graph](count-components%20%28%E8%AE%A1%E6%95%B0%EF%BC%9A%E5%9D%97%E6%95%B0%20%3D%20n%20%E2%88%92%20%E6%88%90%E5%8A%9F%E5%90%88%E5%B9%B6%E6%AC%A1%E6%95%B0%29/LC-0323%20-%20Number%20of%20Connected%20Components%20in%20an%20Undirected%20Graph%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 边列表数连通块（会员） | 并查集计数签名题：块数 = n − 成功合并次数 |
| ○ | [LC 261 Graph Valid Tree](count-components%20%28%E8%AE%A1%E6%95%B0%EF%BC%9A%E5%9D%97%E6%95%B0%20%3D%20n%20%E2%88%92%20%E6%88%90%E5%8A%9F%E5%90%88%E5%B9%B6%E6%AC%A1%E6%95%B0%29/LC-0261%20-%20Graph%20Valid%20Tree) | 边列表是不是一棵树（会员） | 恰好 n−1 条边 + 没有一次 union 失败 |
| ○ | [LC 1319 Number of Operations to Make Network Connected](count-components%20%28%E8%AE%A1%E6%95%B0%EF%BC%9A%E5%9D%97%E6%95%B0%20%3D%20n%20%E2%88%92%20%E6%88%90%E5%8A%9F%E5%90%88%E5%B9%B6%E6%AC%A1%E6%95%B0%29/LC-1319%20-%20Number%20of%20Operations%20to%20Make%20Network%20Connected) | 最少拔插几根网线连通所有电脑 | 线够不够 n−1 + 块数 − 1 |
| ○ | [LC 2316 Count Unreachable Pairs of Nodes in an Undirected Graph](count-components%20%28%E8%AE%A1%E6%95%B0%EF%BC%9A%E5%9D%97%E6%95%B0%20%3D%20n%20%E2%88%92%20%E6%88%90%E5%8A%9F%E5%90%88%E5%B9%B6%E6%AC%A1%E6%95%B0%29/LC-2316%20-%20Count%20Unreachable%20Pairs%20of%20Nodes%20in%20an%20Undirected%20Graph) | 互相不可达的点对数 | 各派 size 两两相乘，练 size 数组的用处 |

## [cycle-by-union (成环：union 返回 False)](cycle-by-union%20%28%E6%88%90%E7%8E%AF%EF%BC%9Aunion%20%E8%BF%94%E5%9B%9E%20False%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 684 Redundant Connection](cycle-by-union%20%28%E6%88%90%E7%8E%AF%EF%BC%9Aunion%20%E8%BF%94%E5%9B%9E%20False%29/LC-0684%20-%20Redundant%20Connection%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 树多了一条边，找出来 | union 返回 False 即成环签名题 |
| △ | [LC 685 Redundant Connection II](cycle-by-union%20%28%E6%88%90%E7%8E%AF%EF%BC%9Aunion%20%E8%BF%94%E5%9B%9E%20False%29/LC-0685%20-%20Redundant%20Connection%20II) | 684 的有向版 | 分"入度为 2"和"有环"两种情况讨论 |
| △ | [LC 1559 Detect Cycles in 2D Grid](cycle-by-union%20%28%E6%88%90%E7%8E%AF%EF%BC%9Aunion%20%E8%BF%94%E5%9B%9E%20False%29/LC-1559%20-%20Detect%20Cycles%20in%202D%20Grid) | 同字符格子能否围成环 | union 相邻同字符格子，失败即有环 |

## [dynamic-add (动态加点、按时间推进)](dynamic-add%20%28%E5%8A%A8%E6%80%81%E5%8A%A0%E7%82%B9%E3%80%81%E6%8C%89%E6%97%B6%E9%97%B4%E6%8E%A8%E8%BF%9B%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ★ | [LC 305 Number of Islands II](dynamic-add%20%28%E5%8A%A8%E6%80%81%E5%8A%A0%E7%82%B9%E3%80%81%E6%8C%89%E6%97%B6%E9%97%B4%E6%8E%A8%E8%BF%9B%29/LC-0305%20-%20Number%20of%20Islands%20II%20-%20%E2%98%85%20%E7%AD%BE%E5%90%8D%E9%A2%98) | 格子逐个变陆地，每次报岛数（会员） | 动态加点 + count ± 1 签名题 |
| ○ | [LC 1101 The Earliest Moment When Everyone Become Friends](dynamic-add%20%28%E5%8A%A8%E6%80%81%E5%8A%A0%E7%82%B9%E3%80%81%E6%8C%89%E6%97%B6%E9%97%B4%E6%8E%A8%E8%BF%9B%29/LC-1101%20-%20The%20Earliest%20Moment%20When%20Everyone%20Become%20Friends) | 按时间顺序交朋友，何时全部连通（会员） | 按时间排序 + union，剩一派时停，这就是 Kruskal 过程的雏形 |
| △ | [LC 2092 Find All People With Secret](dynamic-add%20%28%E5%8A%A8%E6%80%81%E5%8A%A0%E7%82%B9%E3%80%81%E6%8C%89%E6%97%B6%E9%97%B4%E6%8E%A8%E8%BF%9B%29/LC-2092%20-%20Find%20All%20People%20With%20Secret) | 会议按时间发生，秘密传给谁 | 同一时刻的会议一起 union，不知道秘密的人事后"重置"，并查集的进阶用法 |

## [grouping (分组：并查集分派后按组输出)](grouping%20%28%E5%88%86%E7%BB%84%EF%BC%9A%E5%B9%B6%E6%9F%A5%E9%9B%86%E5%88%86%E6%B4%BE%E5%90%8E%E6%8C%89%E7%BB%84%E8%BE%93%E5%87%BA%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ○ | [LC 721 Accounts Merge](grouping%20%28%E5%88%86%E7%BB%84%EF%BC%9A%E5%B9%B6%E6%9F%A5%E9%9B%86%E5%88%86%E6%B4%BE%E5%90%8E%E6%8C%89%E7%BB%84%E8%BE%93%E5%87%BA%29/LC-0721%20-%20Accounts%20Merge) | 有相同邮箱的账户合并 | 邮箱当点，并查集分组后按组输出，面试高频 |
| ○ | [LC 990 Satisfiability of Equality Equations](grouping%20%28%E5%88%86%E7%BB%84%EF%BC%9A%E5%B9%B6%E6%9F%A5%E9%9B%86%E5%88%86%E6%B4%BE%E5%90%8E%E6%8C%89%E7%BB%84%E8%BE%93%E5%87%BA%29/LC-0990%20-%20Satisfiability%20of%20Equality%20Equations) | 一堆 a==b、c!=d 能否同时成立 | 先 union 所有 ==，再逐个检查 != 是否同派 |
| ○ | [LC 1061 Lexicographically Smallest Equivalent String](grouping%20%28%E5%88%86%E7%BB%84%EF%BC%9A%E5%B9%B6%E6%9F%A5%E9%9B%86%E5%88%86%E6%B4%BE%E5%90%8E%E6%8C%89%E7%BB%84%E8%BE%93%E5%87%BA%29/LC-1061%20-%20Lexicographically%20Smallest%20Equivalent%20String) | 字符等价关系下每个位置的最小字符 | 并查集 + 每派记最小代表 |
| ○ | [LC 1202 Smallest String With Swaps](grouping%20%28%E5%88%86%E7%BB%84%EF%BC%9A%E5%B9%B6%E6%9F%A5%E9%9B%86%E5%88%86%E6%B4%BE%E5%90%8E%E6%8C%89%E7%BB%84%E8%BE%93%E5%87%BA%29/LC-1202%20-%20Smallest%20String%20With%20Swaps) | 给定可交换的下标对，字典序最小的串 | 并查集分组，每组内排序回填 |

## [modeling (建模：把别的东西当点)](modeling%20%28%E5%BB%BA%E6%A8%A1%EF%BC%9A%E6%8A%8A%E5%88%AB%E7%9A%84%E4%B8%9C%E8%A5%BF%E5%BD%93%E7%82%B9%29)

| | 题 | 题目在问 | 模板 / 改哪一行 |
|---|---|---|---|
| ○ | [LC 947 Most Stones Removed with Same Row or Column](modeling%20%28%E5%BB%BA%E6%A8%A1%EF%BC%9A%E6%8A%8A%E5%88%AB%E7%9A%84%E4%B8%9C%E8%A5%BF%E5%BD%93%E7%82%B9%29/LC-0947%20-%20Most%20Stones%20Removed%20with%20Same%20Row%20or%20Column) | 同行或同列的石头可以互相消，最多消几个 | 答案 = 石头数 − 块数，行号和列号当点的建模技巧 |
| △ | [LC 952 Largest Component Size by Common Factor](modeling%20%28%E5%BB%BA%E6%A8%A1%EF%BC%9A%E6%8A%8A%E5%88%AB%E7%9A%84%E4%B8%9C%E8%A5%BF%E5%BD%93%E7%82%B9%29/LC-0952%20-%20Largest%20Component%20Size%20by%20Common%20Factor) | 有公因数的数连边，最大连通块多大 | 把质因数当点来 union，建模题 |
| △ | [LC 827 Making A Large Island](modeling%20%28%E5%BB%BA%E6%A8%A1%EF%BC%9A%E6%8A%8A%E5%88%AB%E7%9A%84%E4%B8%9C%E8%A5%BF%E5%BD%93%E7%82%B9%29/LC-0827%20-%20Making%20A%20Large%20Island) | 最多翻一个 0，最大的岛多大 | 先给每块编号记 size，再枚举每个 0 把四周不同块加起来 |
| △ | [LC 1627 Graph Connectivity With Threshold](modeling%20%28%E5%BB%BA%E6%A8%A1%EF%BC%9A%E6%8A%8A%E5%88%AB%E7%9A%84%E4%B8%9C%E8%A5%BF%E5%BD%93%E7%82%B9%29/LC-1627%20-%20Graph%20Connectivity%20With%20Threshold) | 公因数大于阈值才连边，回答查询 | 枚举倍数来 union |

---

每题文件夹：`solution.py`（所有解法 + 复杂度 + ⭐ 最优）、`problem.pdf` / `problem_dark.pdf`、`metadata.json`（复习记录）。
模板在 [00-foundations/templates (模板)](../00-foundations%20%28%E5%9B%BE%E8%AE%BA%E5%9F%BA%E7%A1%80%E3%80%81%E5%9B%BE%E8%AE%BA%E6%89%8B%E5%86%8C%29/templates%20%28%E6%A8%A1%E6%9D%BF%29)，总表在 [../README.md](../README.md)。
