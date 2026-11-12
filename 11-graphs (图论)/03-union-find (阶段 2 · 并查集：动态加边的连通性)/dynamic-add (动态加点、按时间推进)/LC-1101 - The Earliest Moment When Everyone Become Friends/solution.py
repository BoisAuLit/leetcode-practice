"""LC-1101 - The Earliest Moment When Everyone Become Friends

阶段 2 · 并查集动态加点、按时间推进 ○ 核心
题目在问：按时间顺序交朋友（朋友的朋友也算认识），最早在哪个时刻所有人都互相认识
点是什么：n 个人   边是什么：logs 里的每条 (时间, x, y)，按时间从早到晚一条条加
和签名题比改了哪一行：和 323 比，边先按时间排序再 union，块数降到 1 的那一刻返回时间；这就是 Kruskal 过程的雏形
"""
from typing import List


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
##### ! Solution 1: 按时间排序 + Union-Find，UF 内部的 count 降到 1 就停
##### ! 时间复杂度: O(m log m + m · α(n))（m = len(logs)，排序占大头）   空间复杂度: O(n)
##### ! 适用：事件带时间戳、问"何时全部连通"；边按某个 key 排序后依次 union，就是 Kruskal 的过程骨架
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################

class Solution:
    def earliestAcq(self, logs: List[List[int]], n: int) -> int:
        logs.sort()
        uf = UnionFind(n)
        for time, x, y in logs:
            uf.union(x, y)
            if uf.getCount() == 1:
                return time
        return -1


##################################################################################################
##### ! Solution 2: 同一思路，用"块数 = n − 成功合并次数"自己数（323 的签名写法）
##### ! 时间复杂度: O(m log m + m · α(n))   空间复杂度: O(n)
##### ! 适用：同 Solution 1；union 返回 bool 时不用在 UF 里藏 count，Kruskal（1135 / 1584）也是这样数"用了几条边"
##################################################################################################


class UnionFindBool:  # 和 1135 参考文件里的模板一样：路径减半 + 按 size 合并，union 返回 bool
    def __init__(self, n: int):  # 上面用户自己的 UnionFind 名字已占用，所以另起一个名
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
    def earliestAcq(self, logs: List[List[int]], n: int) -> int:
        uf = UnionFindBool(n)
        groups = n  # ! 一开始 n 个人各自一派
        for t, x, y in sorted(logs):  # ! 按时间推进
            if uf.union(x, y):  # ! 成功合并才少一派
                groups -= 1
                if groups == 1:
                    return t
        return -1


s = Solution()
logs = [[20190101, 0, 1], [20190104, 3, 4], [20190107, 2, 3], [20190211, 1, 5],
        [20190224, 2, 4], [20190301, 0, 3], [20190312, 1, 2], [20190322, 4, 5]]
n = 6
result = s.earliestAcq(logs, n)
print(result)  # 20190301
result = s.earliestAcq([[0, 2, 0], [1, 0, 1], [3, 0, 3], [4, 1, 2], [7, 3, 1]], 4)
print(result)  # 3
