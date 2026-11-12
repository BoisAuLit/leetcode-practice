"""LC-0547 - Number of Provinces

阶段 1 · DFS、BFS（静态无权的连通性与步数）· 洪水填充（数连通块）○ 核心
题目在问：邻接矩阵表示的朋友圈有几个（连通分量个数）
点是什么：一个城市   边是什么：isConnected[i][j] == 1
和签名题比改了哪一行：和 200 的区别只是图的存法，邻居不是上下左右而是扫矩阵第 i 行；数连通块的外层循环一模一样
"""
from typing import List
from collections import deque


##################################################################################################
##### ! Solution 1: 并查集（按 rank 合并 + 递归路径压缩）
##### ! 时间复杂度: O(n²·α(n))   空间复杂度: O(n)
##### ! 适用：边是动态加进来、要边加边查连通时（阶段 2 的模板）；静态矩阵它和 DFS 一样快，只是代码更长
##################################################################################################


class UnionFind:
    def __init__(self, n: int):
        self.root = list(range(n))
        self.rank = [1] * n
        self.count = n

    def find(self, x: int) -> int:
        if self.root[x] == x:
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


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        uf = UnionFind(n)
        for i in range(n - 1):
            for j in range(i + 1, n):
                if isConnected[i][j]:
                    uf.union(i, j)
        return uf.getCount()


##################################################################################################
##### ! Solution 2: 递归 DFS 数连通块
##### ! 时间复杂度: O(n²)   空间复杂度: O(n)
##### ! 适用：阶段 1 的模板本身，最短；和 200 唯一的区别是邻居从四方向换成扫第 i 行。n ≤ 200 递归不会爆
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_2:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        visited = [False] * n

        def dfs(i: int) -> None:
            visited[i] = True
            for j in range(n):  # ! 邻居 = 第 i 行里为 1 的列，这是和 200 唯一的区别
                if isConnected[i][j] and not visited[j]:
                    dfs(j)

        count = 0
        for i in range(n):
            if not visited[i]:  # ! 每遇到一个没访问过的点，就是一个新省份
                count += 1
                dfs(i)
        return count


##################################################################################################
##### ! Solution 3: BFS 数连通块
##### ! 时间复杂度: O(n²)   空间复杂度: O(n)
##### ! 适用：和 Solution 2 等价，不怕递归深度；入队时立即标记
##################################################################################################


class Solution_3:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        visited = [False] * n
        count = 0
        for i in range(n):
            if visited[i]:
                continue
            count += 1  # ! 新省份
            visited[i] = True
            q = deque([i])
            while q:
                u = q.popleft()
                for v in range(n):
                    if isConnected[u][v] and not visited[v]:
                        visited[v] = True  # ! 入队时立即标记
                        q.append(v)
        return count


s = Solution()
isConnected = [[1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1], [1, 0, 1, 1]]
result = s.findCircleNum(isConnected)
print(result)
