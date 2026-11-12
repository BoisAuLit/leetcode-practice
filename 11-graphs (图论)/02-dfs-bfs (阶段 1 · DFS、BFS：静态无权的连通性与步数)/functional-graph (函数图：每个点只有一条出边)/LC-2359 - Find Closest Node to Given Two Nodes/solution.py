"""LC-2359 - Find Closest Node to Given Two Nodes

阶段 1 · 函数图：每个点只有一条出边 △ 扩展
题目在问：从 node1 和 node2 出发都能到的点里，找 max(d1, d2) 最小的那个；并列取下标最小；没有返回 -1
点是什么：一个节点   边是什么：i -> edges[i]（每个点最多一条出边，-1 表示没有）
和签名题比改了哪一行：200 的 DFS 要递归/栈去处理分叉；函数图上每个点只有一条出边，
    从起点出发的路径是唯一的，"遍历"退化成一个 while 沿 edges 往前走，走到 -1 或走回走过的点就停。
    两次 walk 得到 d1、d2，再按下标扫一遍取最优
"""
from math import inf
from typing import List

##################################################################################################
##### ! Solution 1: 沿唯一出边走两次记距离，再扫一遍取 max(d1, d2) 最小
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：函数图（出度 <= 1）上的单源距离。只有这一种写法：
##### !       每个点只有一条出边，从起点出发的路径唯一，DFS/BFS 的"分叉 + 回溯 / 队列"根本用不上，
##### !       一个 while 循环就是完整的遍历，也不存在递归深度问题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def closestMeetingNode(self, edges: List[int], node1: int, node2: int) -> int:
        n = len(edges)

        def distances(start: int) -> List[int]:
            # ! 从 start 沿唯一出边走，dist[u] = 第几步走到 u；-1 = 到不了
            dist = [-1] * n
            u, d = start, 0
            while u != -1 and dist[u] == -1:  # ! 走到断头(-1) 或 走回走过的点(进环) 就停
                dist[u] = d
                d += 1
                u = edges[u]
            return dist

        d1, d2 = distances(node1), distances(node2)
        ans, best = -1, inf
        for i in range(n):  # ! 按下标从小到大扫，严格小于才更新，并列自然留最小下标
            if d1[i] != -1 and d2[i] != -1 and max(d1[i], d2[i]) < best:
                best = max(d1[i], d2[i])
                ans = i
        return ans


s = Solution_1()
edges = [2, 2, 3, -1]
node1 = 0
node2 = 1
result = s.closestMeetingNode(edges, node1, node2)
print(result)  # 2

edges = [1, 2, -1]
node1 = 0
node2 = 2
result = s.closestMeetingNode(edges, node1, node2)
print(result)  # 2
