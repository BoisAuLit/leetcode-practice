"""LC-1627 - Graph Connectivity With Threshold

阶段 2 · 并查集建模 (把别的东西当点) △ 扩展
题目在问：城市 1..n，两城有某个公因数 z > threshold 就有路；回答若干 (a, b) 能否互达
点是什么：城市 1..n   边是什么：gcd(a, b) > threshold (隐式边，O(n^2) 条，不能真的枚举)
和签名题比改了哪一行：323 的边是直接给的；这里改成枚举"公因数 z"本身：
                      对每个 z > threshold，把 z, 2z, 3z, ... 全 union 到一起 (调和级数，总共 O(n log n) 次)
"""
from typing import List


class UnionFind:  # 路径减半 + 按 size 合并，union 返回 bool
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


##################################################################################################
##### ! Solution 1: Union-Find，按公因数枚举倍数
##### ! 时间复杂度: O(n log n · α(n) + q)   空间复杂度: O(n)
##### ! 适用：边太多但"边的成因" (公因数) 很少时，枚举成因而不是枚举边
##### ! 为什么只写一种：暴力枚举 n^2/2 对 + gcd 是 1e8 量级直接超时；DFS/BFS 也只能靠同样的
##### ! "枚举倍数"来找邻居，等于并查集换个壳、代码更长，所以没有第二种值得写的解法
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def areConnected(self, n: int, threshold: int, queries: List[List[int]]) -> List[bool]:
        uf = UnionFind(n + 1)  # 多开一格：下标 0 闲置，城市 1..n 直接用
        for z in range(threshold + 1, n + 1):
            # ! z 的所有倍数两两都有公因数 z > threshold，串成一派；z > n/2 时 range 为空自动跳过
            # ! 合数 z 也要枚举：threshold = 3 时 4 和 8 靠公因数 4 相连，但 4 不是质数
            for mult in range(2 * z, n + 1, z):
                uf.union(z, mult)
        return [uf.find(a) == uf.find(b) for a, b in queries]


s = Solution_1()
n = 6
threshold = 2
queries = [[1, 4], [2, 5], [3, 6]]
result = s.areConnected(n, threshold, queries)
print(result)  # [False, False, True]
print(Solution_1().areConnected(6, 0, [[4, 5], [3, 4], [3, 2], [2, 6], [1, 3]]))  # [True, True, True, True, True]
print(Solution_1().areConnected(5, 1, [[4, 5], [4, 5], [3, 2], [2, 3], [3, 4]]))  # [False, False, False, False, False]
