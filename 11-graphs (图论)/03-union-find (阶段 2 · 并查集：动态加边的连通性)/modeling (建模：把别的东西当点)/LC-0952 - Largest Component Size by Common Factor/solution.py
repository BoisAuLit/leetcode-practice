"""LC-0952 - Largest Component Size by Common Factor

阶段 2 · 并查集建模 (把别的东西当点) △ 扩展
题目在问：数组里两个数有公因数 (> 1) 就连边，最大的连通块里有几个数
点是什么：每个数 + 每个质因数   边是什么：数 和 它的每个质因数 之间连一条
和签名题比改了哪一行：323 是 union(a, b) 把两个点连起来；这里不能枚举数对 (O(n^2) 个 gcd 太慢)，
                      改成 union(num, 质因数 p)：两个数共用一个质因数就自动同派，最后只数"原数组里的数"落在哪个根下
"""
from collections import Counter, defaultdict, deque
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
##### ! Solution 1: Union-Find + 试除分解质因数
##### ! 时间复杂度: O(n · √M + n · α(M))   空间复杂度: O(M)，M = max(nums)
##### ! 适用：面试里最常写的版本，不用预处理；n = 2e4、M = 1e5 时 √M 约 316，够快
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution (和 Solution 2 思路完全一样，这个更短更常考，所以选它)
##################################################################################################


class Solution_1:
    def largestComponentSize(self, nums: List[int]) -> int:
        uf = UnionFind(max(nums) + 1)  # 下标直接当"值"用：数和质因数都是 0..M 里的点
        for num in nums:
            x, p = num, 2
            while p * p <= x:  # 试除：每找到一个质因数就把 num 挂到它上面
                if x % p == 0:
                    uf.union(num, p)
                    while x % p == 0:
                        x //= p
                p += 1
            if x > 1:  # ! 剩下的 x 是最后一个质因数 (num 是质数时就是它自己)
                uf.union(num, x)

        # ! 只数原数组里的数：质因数只是"桥"，不算人头 (uf.size 里混着桥，不能直接用)
        cnt = Counter(uf.find(num) for num in nums)
        return max(cnt.values())


##################################################################################################
##### ! Solution 2: Union-Find + 最小质因数筛 (SPF)
##### ! 时间复杂度: O(M log log M + n log M + n · α(M))   空间复杂度: O(M)
##### ! 适用：分解质因数从 O(√M) 降到 O(log M)，数很多、值域不大时明显更快
##################################################################################################


class Solution_2:
    def largestComponentSize(self, nums: List[int]) -> int:
        m = max(nums)
        spf = list(range(m + 1))  # spf[x] = x 的最小质因数，先假设是自己
        for i in range(2, int(m ** 0.5) + 1):
            if spf[i] == i:  # i 是质数：它的倍数里还没被标过的，最小质因数就是 i
                for j in range(i * i, m + 1, i):
                    if spf[j] == j:
                        spf[j] = i

        uf = UnionFind(m + 1)
        for num in nums:
            x = num
            while x > 1:  # ! 顺着 spf 一路除，每轮剥掉一个质因数
                p = spf[x]
                uf.union(num, p)
                while x % p == 0:
                    x //= p
        cnt = Counter(uf.find(num) for num in nums)
        return max(cnt.values())


##################################################################################################
##### ! Solution 3: BFS on "数 - 质因数" 二分图
##### ! 时间复杂度: O(n · √M + n log M)   空间复杂度: O(n log M)
##### ! 适用：图是静态的，所以 BFS 也行：数 -> 它的质因数 -> 共用这个质因数的其他数；并查集只是更短
##################################################################################################


class Solution_3:
    def largestComponentSize(self, nums: List[int]) -> int:
        primes_of = {}  # 数 -> 它的质因数列表
        by_prime = defaultdict(list)  # 质因数 -> 含它的数
        for num in nums:
            x, p, ps = num, 2, []
            while p * p <= x:
                if x % p == 0:
                    ps.append(p)
                    while x % p == 0:
                        x //= p
                p += 1
            if x > 1:
                ps.append(x)
            primes_of[num] = ps
            for p in ps:
                by_prime[p].append(num)

        visited = set()
        best = 0
        for s in nums:
            if s in visited:
                continue
            visited.add(s)
            q = deque([s])
            sz = 0
            while q:
                u = q.popleft()
                sz += 1
                for p in primes_of[u]:
                    for v in by_prime[p]:
                        if v not in visited:
                            visited.add(v)
                            q.append(v)
                    by_prime[p] = []  # ! 这个质因数的名单整个入队了，清空，别让它被反复扫
            best = max(best, sz)
        return best


s = Solution_1()
nums = [4, 6, 15, 35]
result = s.largestComponentSize(nums)
print(result)  # 4
print(Solution_1().largestComponentSize([20, 50, 9, 63]))  # 2
print(Solution_1().largestComponentSize([2, 3, 6, 7, 4, 12, 21, 39]))  # 8
