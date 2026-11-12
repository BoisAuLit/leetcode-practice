"""LC-1203 - Sort Items by Groups Respecting Dependencies

阶段 3 · DAG 上的 DP（拓扑序 + 状态转移） △ 扩展
题目在问：n 个 item 分属 m 个组（-1 = 没组），有 item 之间的先后依赖；
          求一个排列：同组的 item 挨在一起，且所有依赖都满足；不存在返回 []
点是什么：两层。item 图的点是 item，组图的点是组
边是什么：beforeItems[v] 里的每个 u 给 item 图一条 u -> v；u、v 不同组时再给组图一条 group[u] -> group[v]
和签名题比改了哪一行：207 的 Kahn 做两遍（item 图一遍、组图一遍），任一遍没出完队就是 []；
                     多一步预处理：没组的 item 各发一个新组号，让它自己独占一组
"""
from collections import deque
from typing import List

##################################################################################################
##### ! Solution 1: 两次 Kahn（item 图整体排一次 + 组图排一次），再按组装桶
##### ! 时间复杂度: O(n + m + E)，E = 所有 beforeItems 的总长度   空间复杂度: O(n + m + E)
##### ! 适用：两层依赖的标准解；画面：先把所有 item 排成一条合法的拓扑序，再按组的拓扑序把这条序"分桶倒出来"
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def sortItems(self, n: int, m: int, group: List[int], beforeItems: List[List[int]]) -> List[int]:
        group = group[:]
        g = m
        for i in range(n):
            if group[i] == -1:  # ! 没组的 item 各发一个新组号，组数从 m 涨到 g
                group[i] = g
                g += 1

        item_adj = [[] for _ in range(n)]
        item_indeg = [0] * n
        grp_adj = [set() for _ in range(g)]  # set 去重：两组之间多条依赖只算一条边
        grp_indeg = [0] * g
        for v in range(n):
            for u in beforeItems[v]:
                item_adj[u].append(v)
                item_indeg[v] += 1
                gu, gv = group[u], group[v]
                if gu != gv and gv not in grp_adj[gu]:  # ! 跨组依赖才变成组图的边
                    grp_adj[gu].add(gv)
                    grp_indeg[gv] += 1

        def kahn(adj, indeg) -> List[int]:  # 207 原封不动，没出完队返回 None
            q = deque(x for x in range(len(adj)) if indeg[x] == 0)
            order = []
            while q:
                x = q.popleft()
                order.append(x)
                for y in adj[x]:
                    indeg[y] -= 1
                    if indeg[y] == 0:
                        q.append(y)
            return order if len(order) == len(adj) else None

        item_order = kahn(item_adj, item_indeg)
        grp_order = kahn(grp_adj, grp_indeg)
        if item_order is None or grp_order is None:
            return []  # 任一层有环

        bucket = [[] for _ in range(g)]
        for x in item_order:  # ! 按 item 拓扑序丢进各自的桶，桶内自然是合法顺序
            bucket[group[x]].append(x)
        return [x for gi in grp_order for x in bucket[gi]]  # 按组的拓扑序倒出来


##################################################################################################
##### ! Solution 2: 先排组，再在每个组内部单独做 Kahn
##### ! 时间复杂度: O(n + m + E)   空间复杂度: O(n + m + E)
##### ! 适用：更贴近"两层"的直觉写法：item 图只保留同组内的边，跨组的边全部交给组图去管；
##### !       跨组的环一定会在组图里现形，同组的环在组内 Kahn 里现形
##################################################################################################


class Solution_2:
    def sortItems(self, n: int, m: int, group: List[int], beforeItems: List[List[int]]) -> List[int]:
        group = group[:]
        g = m
        for i in range(n):
            if group[i] == -1:
                group[i] = g
                g += 1
        members = [[] for _ in range(g)]
        for i in range(n):
            members[group[i]].append(i)

        item_adj = [[] for _ in range(n)]  # ! 只存同组内的边
        item_indeg = [0] * n
        grp_adj = [set() for _ in range(g)]
        grp_indeg = [0] * g
        for v in range(n):
            for u in beforeItems[v]:
                gu, gv = group[u], group[v]
                if gu == gv:
                    item_adj[u].append(v)
                    item_indeg[v] += 1
                elif gv not in grp_adj[gu]:
                    grp_adj[gu].add(gv)
                    grp_indeg[gv] += 1

        def kahn(nodes, adj, indeg) -> List[int]:  # 只在 nodes 这个子集上跑
            q = deque(x for x in nodes if indeg[x] == 0)
            order = []
            while q:
                x = q.popleft()
                order.append(x)
                for y in adj[x]:
                    indeg[y] -= 1
                    if indeg[y] == 0:
                        q.append(y)
            return order if len(order) == len(nodes) else None

        grp_order = kahn(range(g), grp_adj, grp_indeg)
        if grp_order is None:
            return []
        ans = []
        for gi in grp_order:  # 按组的拓扑序，每个组内部再排一次
            part = kahn(members[gi], item_adj, item_indeg)
            if part is None:
                return []
            ans += part
        return ans


# ! LeetCode 示例答案是 [6, 3, 4, 1, 5, 2, 0, 7]；这里会打印另一个合法顺序，LeetCode 接受任一合法答案
s = Solution_1()
n = 8
m = 2
group = [-1, -1, 1, 0, 0, 1, 0, -1]
beforeItems = [[], [6], [5], [6], [3, 6], [], [], []]
result = s.sortItems(n, m, group, beforeItems)
print(result)  # [6, 3, 4, 0, 7, 1, 5, 2] 之类的合法顺序
