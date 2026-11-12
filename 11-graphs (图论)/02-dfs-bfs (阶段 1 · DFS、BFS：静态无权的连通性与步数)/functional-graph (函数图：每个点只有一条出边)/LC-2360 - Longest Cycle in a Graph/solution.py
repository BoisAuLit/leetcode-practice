"""LC-2360 - Longest Cycle in a Graph

阶段 1 · 函数图：每个点只有一条出边 △ 扩展
题目在问：有向图里每个点最多一条出边，最长的环有几个点；没有环返回 -1
点是什么：一个节点   边是什么：i -> edges[i]（-1 表示没出边）
和签名题比改了哪一行：函数图上从一个没走过的点出发沿唯一出边走就是一条链，链的尽头要么是 -1，
    要么撞上走过的点。给每个点记"第一次走到它的时间戳"（全局递增，每条链一个起始时间）：
    撞上的点如果是本次这条链上的（时间戳 >= 本次起始时间），环长 = 当前时间 - 它的时间戳；
    撞上的是以前链上的点，只是汇入旧路，没有新环。
    和 2359 比：2359 记的是距离，这里把距离换成全局时间戳，顺便区分"本次链 / 以前的链"
"""
from collections import deque
from typing import List

##################################################################################################
##### ! Solution 1: 沿唯一出边走 + 时间戳
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：函数图找环的标准写法；每个点只被走一次，撞到本次链上的点立刻得到环长
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def longestCycle(self, edges: List[int]) -> int:
        n = len(edges)
        time = [0] * n  # ! 0 = 没走过；否则 = 第一次走到它的时间戳（全局递增，不同链不重叠）
        clock = 1
        ans = -1
        for i in range(n):
            if time[i]:
                continue
            start = clock  # ! 本次这条链的起始时间，用来判断撞上的点是不是本次链上的
            u = i
            while u != -1 and time[u] == 0:
                time[u] = clock
                clock += 1
                u = edges[u]
            # ! 停下来有两种情况：u == -1 断头 / u 是走过的点
            # ! 走过的点若 time[u] >= start，说明是本次链上的，从 u 到链尾正好是一个环
            if u != -1 and time[u] >= start:
                ans = max(ans, clock - time[u])
        return ans


##################################################################################################
##### ! Solution 2: 拓扑剥皮（Kahn）：剥掉所有入度 0 的点，剩下的全在环上，再逐个量环长
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：想不起时间戳时的兜底写法；两遍扫描，先剥链再量环
##################################################################################################


class Solution_2:
    def longestCycle(self, edges: List[int]) -> int:
        n = len(edges)
        indeg = [0] * n
        for v in edges:
            if v != -1:
                indeg[v] += 1
        queue = deque(i for i in range(n) if indeg[i] == 0)  # ! 没人指向的点一定不在环上
        removed = [False] * n
        while queue:
            u = queue.popleft()
            removed[u] = True
            v = edges[u]
            if v != -1:
                indeg[v] -= 1
                if indeg[v] == 0:  # ! u 剥掉后 v 也没人指了，继续剥
                    queue.append(v)
        # ! 剩下的点：入度 >= 1 且出度 = 1，点数 = 边数，只能是若干个不相交的纯环
        ans = -1
        visited = [False] * n
        for i in range(n):
            if removed[i] or visited[i]:
                continue
            length = 0
            u = i
            while not visited[u]:  # ! 绕环一圈数点数
                visited[u] = True
                length += 1
                u = edges[u]
            ans = max(ans, length)
        return ans


s = Solution_1()
edges = [3, 3, 4, 2, 3]
result = s.longestCycle(edges)
print(result)  # 3

edges = [2, -1, 3, 1]
result = s.longestCycle(edges)
print(result)  # -1
