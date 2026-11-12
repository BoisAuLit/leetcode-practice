"""LC-1202 - Smallest String With Swaps

阶段 2 · 并查集分组 ○ 核心
题目在问：给定可以任意次交换的下标对，能得到的字典序最小的字符串
点是什么：下标 0..n-1   边是什么：pairs 里的每一对下标（可交换 = 连通，同一块内的字符可以任意重排）
和签名题比改了哪一行：和 323 比，union 完不数块数，而是按 find(i) 把下标分组，每组字符排序后回填
"""
from typing import List
from collections import defaultdict


class UnionFind:
    def __init__(self, n: int):
        self.root = list(range(n))
        self.rank = [1] * n
        self.count = n

    def find(self, x: int) -> int:
        if x == self.root[x]:
            return x
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x: int, y: int):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.root[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.root[rootX] = rootY
            else:
                self.root[rootY] = rootX
                self.rank[rootX] += 1
            self.count -= 1

    def getCount(self) -> int:
        return self.count

    def isConnected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


##################################################################################################
##### ! Solution 1: Union-Find 分组 + 每组排序回填
##### ! 时间复杂度: O((n + m) · α(n) + n log n)（m = len(pairs)，各组排序合计 n log n）   空间复杂度: O(n)
##### ! 适用：只给"谁和谁可换"的下标对、不想建邻接表；关键画面是同一块内的字符可以任意重排
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################

class Solution:
    """
    Principle:
    Locate all the letter in the same component.
    Sort letters in ascending order in that component.
    Re-put those sorted letters in the origianl sting.
    """
    def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
        n = len(s)
        uf = UnionFind(n)
        for x, y in pairs:
            uf.union(x, y)
        components = defaultdict(list)
        for i in range(n):
            components[uf.find(i)].append(i)
        result = [0] * n
        for component_indices in components.values():
            letters = sorted([s[i] for i in component_indices])
            for i, j in enumerate(component_indices):
                result[j] = letters[i]
        return "".join(result)


##################################################################################################
##### ! Solution 2: DFS 分组（建邻接表，迭代栈走完一块就拿到这一组下标）
##### ! 时间复杂度: O(n + m + n log n)   空间复杂度: O(n + m)
##### ! 适用：静态图、想顺便拿到每组下标；n 到 1e5 所以用迭代栈不用递归
##################################################################################################


class Solution_2:
    def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
        n = len(s)
        adj = [[] for _ in range(n)]
        for a, b in pairs:
            adj[a].append(b)
            adj[b].append(a)

        seen = [False] * n
        result = list(s)
        for start in range(n):
            if seen[start]:
                continue
            seen[start] = True
            stack, group = [start], []
            while stack:  # ! 迭代 DFS，走完一块就是一组下标
                i = stack.pop()
                group.append(i)
                for j in adj[i]:
                    if not seen[j]:
                        seen[j] = True
                        stack.append(j)
            group.sort()  # ! 下标从小到大、字符从小到大，一一对应回填
            for i, ch in zip(group, sorted(s[i] for i in group)):
                result[i] = ch
        return "".join(result)


solution = Solution()
s = "dcab"
pairs = [[0, 3], [1, 2]]
result = solution.smallestStringWithSwaps(s, pairs)
print(result)
