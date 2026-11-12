"""LC-1557 - Minimum Number of Vertices to Reach All Nodes

阶段 3 · Kahn（按入度做 BFS） ○ 核心
题目在问：DAG 里最少从哪些点出发，能走到图上所有点（题目保证答案唯一）
点是什么：0..n-1   边是什么：edges 里的 [u, v] 是一条 u -> v
和签名题比改了哪一行：只用了 207 的第一步"数入度"，队列都不用开：入度为 0 的点就是答案
"""
from typing import List

##################################################################################################
##### ! Solution 1: 数入度
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V)
##### ! 适用：DAG 上的"最少起点"问题。两句话证明：
##### !   必要：入度 0 的点没有任何人能走到它，只能自己当起点
##### !   充分：入度 > 0 的点沿着入边一直往回走，DAG 没环所以走不了无限步，最后一定停在某个入度 0 的点
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findSmallestSetOfVertices(self, n: int, edges: List[List[int]]) -> List[int]:
        indeg = [0] * n
        for _, v in edges:
            indeg[v] += 1  # ! 只关心"有没有人指向我"，谁指的不重要
        return [u for u in range(n) if indeg[u] == 0]


##################################################################################################
##### ! Solution 2: 集合差（一行版）
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V)
##### ! 适用：同上，口述时的最短写法：所有点 减去 被指过的点
##################################################################################################


class Solution_2:
    def findSmallestSetOfVertices(self, n: int, edges: List[List[int]]) -> List[int]:
        return sorted(set(range(n)) - {v for _, v in edges})


s = Solution_1()
n = 6
edges = [[0, 1], [0, 2], [2, 5], [3, 4], [4, 2]]
result = s.findSmallestSetOfVertices(n, edges)
print(result)  # [0, 3]
