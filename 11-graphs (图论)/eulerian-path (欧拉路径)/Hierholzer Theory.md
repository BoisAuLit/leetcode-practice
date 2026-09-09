# Hierholzer's Algorithm（Eulerian path / circuit）

存在条件
- 无向图：连通，且奇度点个数为 0（回路）或 2（路径，从一个奇度点出发）
- 有向图：连通，且除起点 (out − in = 1) 和终点 (in − out = 1) 外所有点 in == out；全部相等 ⇒ 回路

算法（O(E)）
1. 从起点出发，沿着还没用过的边一直走（每走一条边就把它删掉），走到死路为止
2. 死路的点 append 到结果（post-order）
3. 回溯：回到上一个还有未用边的点，继续走
4. 最后把结果 reverse

为什么对：走到死路的点一定是整条路线的终点（或后段），先放进去再反转，卡住的点自然排在最后。

0332 的细节
- 邻居按字典序：reverse 排序后 `pop()` 取最小 → 字典序最小的行程
- 递归版：`while graph[node]: dfs(graph[node].pop()); itinerary.append(node)`
- 迭代版：stack；栈顶还有边就 push 它 pop 出的邻居，否则把栈顶弹到 itinerary；最后 reverse
