"""LC-0685 - Redundant Connection II

阶段 2 · 并查集成环 △ 扩展
题目在问：一棵有根树（每点入度 ≤ 1，根入度 0）多加了一条有向边，删哪条能变回有根树（多解时取输入里最后出现的）
点是什么：1..n 的编号   边是什么：edges 里的有向边 u → v（u 是 v 的父亲）
和签名题比改了哪一行：和 684 比多了"方向"：先找入度为 2 的点拿到两条候选边，跳过后一条再跑 684；
  union 失败 → 答前一条（没有候选边就是纯环，答第一次失败的那条）；没失败 → 答后一条

⚠️ 文件夹名 / metadata 写的是 LC-0685，但下面用户原有的 class Solution 和 problem.pdf 都是
   LC-0658 Find K Closest Elements 的内容（提交记录里这个文件夹一直在 05-binary-search/peak-and-closest 下，
   应该是 0658 / 0685 两个编号打错了）。用户代码原样保留；LC-0685 的解法从 Solution_2 开始。
"""
from typing import List
from bisect import bisect_left
from collections import deque


##################################################################################################
##### ! Solution 1: 二分定位 + 双指针向两边扩（这是 LC-0658 Find K Closest Elements 的解法）
##### ! 时间复杂度: O(log n + k)   空间复杂度: O(k)
##### ! 适用：有序数组里取离 x 最近的 k 个；和本文件夹标的 LC-0685 无关
##################################################################################################
# ! ⚠️ 这里有问题：这个 class 解的是 LC-0658（findClosestElements），不是 LC-0685 Redundant Connection II；
# !    代码本身是对的，只是题目归错了文件夹（见文件头）。LC-0685 的解法见下面的 Solution_2 / Solution_3。
class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        n = len(arr)
        left = bisect_left(arr, x) - 1 # This is very crucial
        right = left + 1
        result = deque()
        while len(result) != k:
            d1 = d2 = float("inf")
            if 0 <= left <= n - 1:
                d1 = abs(arr[left] - x)
            if 0 <= right <= n - 1:
                d2 = abs(arr[right] - x)
            if d1 <= d2:
                result.appendleft(arr[left])
                left -= 1
            else:
                result.append(arr[right])
                right += 1
        return list(result)


##################################################################################################
##### ! Solution 2: Union-Find 三种情况（入度为 2 → 两条候选边；跳过后一条再跑 684）
##### ! 时间复杂度: O(n · α(n))   空间复杂度: O(n)
##### ! 适用：本题标准解；画面是"先把方向信息（入度）榨干，剩下的交给 684"
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class UnionFind:  # 和 1135 参考文件里的模板一样：路径减半 + 按 size 合并，union 返回 bool
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # ! 路径减半：每走一步就往上跳一级
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False  # ! 已经同一派，合并失败
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


class Solution_2:
    def findRedundantDirectedConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        parent = [0] * (n + 1)  # parent[v] = 第一条进入 v 的边的起点，0 表示还没有入边
        cand1 = cand2 = None  # ! 入度为 2 的点的两条入边：cand1 先出现，cand2 后出现
        skip = -1  # cand2 在 edges 里的下标
        for i, (u, v) in enumerate(edges):
            if parent[v] == 0:
                parent[v] = u
            else:
                cand1, cand2, skip = [parent[v], v], [u, v], i
                break  # ! 最多只有一个入度为 2 的点（多了就不可能只删一条边变回树）

        uf = UnionFind(n + 1)
        for i, (u, v) in enumerate(edges):
            if i == skip:  # ! 先假设多余的是后一条候选边，不加它
                continue
            if not uf.union(u, v):  # ! 还是成环
                return cand1 if cand1 else [u, v]  # ! 有候选边：环在前一条上，答前一条；没候选边：纯环，答这条
        return cand2  # ! 跳过后一条就无环了，多余的就是它


##################################################################################################
##### ! Solution 3: 枚举删哪条边 + 验证剩下的是不是有根树（暴力，用来兜底 / 对拍）
##### ! 时间复杂度: O(n²)   空间复杂度: O(n)
##### ! 适用：n ≤ 1000 能过；想不起三种情况时，"从后往前试删、验有根树"是最不容易写错的
##################################################################################################


class Solution_3:
    def findRedundantDirectedConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)

        def is_rooted_tree(skip: int) -> bool:  # 去掉第 skip 条边后，剩下的是不是一棵有根树
            indeg = [0] * (n + 1)
            adj = [[] for _ in range(n + 1)]
            for i, (u, v) in enumerate(edges):
                if i != skip:
                    indeg[v] += 1
                    adj[u].append(v)
            roots = [v for v in range(1, n + 1) if indeg[v] == 0]
            if len(roots) != 1 or max(indeg) > 1:  # ! 恰好一个根，且每个点最多一个父亲
                return False
            seen = {roots[0]}
            stack = [roots[0]]
            while stack:  # ! 从根出发要能走遍所有点
                u = stack.pop()
                for v in adj[u]:
                    if v not in seen:
                        seen.add(v)
                        stack.append(v)
            return len(seen) == n

        for i in range(n - 1, -1, -1):  # ! 从后往前试，第一个能成树的就是"最后出现"的答案
            if is_rooted_tree(i):
                return edges[i]
        return []


# # Test case 1: Expecting [1, 1, 2, 3]
# s = Solution()
# arr = [1, 1, 2, 3, 4, 5]
# k = 4
# x = -1
# result = s.findClosestElements(arr, k, x)
# print(result)

# ! ------------------------------------------------

# # Test case 2: Expecting [1, 2, 3, 4]
# s = Solution()
# arr = [1, 2, 3, 4, 5]
# k = 4
# x = 3
# result = s.findClosestElements(arr, k, x)
# print(result)

# ! ------------------------------------------------

# # Test case 3: Expecting [10]
# s = Solution()
# arr = [1, 1, 1, 10, 10, 10]
# k = 1
# x = 9
# result = s.findClosestElements(arr, k, x)
# print(result)

# ! ------------------------------------------------

# # Test case 4: Expecting [1,1,2,3,3,3]
# s = Solution()
# arr = [1, 1, 2, 3, 3, 3, 4, 6, 8, 8]
# k = 6
# x = 1
# result = s.findClosestElements(arr, k, x)
# print(result)

# ! ------------------------------------------------

# # Test case 5: Expecting [2,3,3]
# s = Solution()
# arr = [1,1,2,2,2,2,2,3,3]
# k = 3
# x = 3
# result = s.findClosestElements(arr, k, x)
# print(result)

# ! ------------------------------------------------

# # Test case 5: Expecting [3,3,4]
# s = Solution()
# arr = [0, 0, 1, 2, 3, 3, 4, 7, 7, 8]
# k = 3
# x = 5
# result = s.findClosestElements(arr, k, x)
# print(result)


# ! ------------------------------------------------
# LC-0685 的例子（用 Preferred 的 Solution_2）
s = Solution_2()
edges = [[1, 2], [1, 3], [2, 3]]
result = s.findRedundantDirectedConnection(edges)
print(result)  # [2, 3]
result = s.findRedundantDirectedConnection([[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]])
print(result)  # [4, 1]
