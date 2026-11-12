"""LC-0305 - Number of Islands II

阶段 2 · 并查集 · 动态加点（按时间推进） ★ 签名题
题目在问：m×n 的海里格子一个一个变成陆地，每加完一格就报一次岛数
点是什么：一个格子 (r, c)，编号 r·n + c   边是什么：上下左右相邻且两边都是陆地
和签名题比改了哪一行：本题就是签名题。核心两行：新格子先当一座新岛 count += 1，
                      再和四周已有陆地 union，每成功一次 count -= 1；重复加同一格岛数不变
"""
from typing import List


class UnionFind:  # 路径减半 + 按 size 合并，union 返回 bool（成功合并才 True）
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
##### ! Solution 1: Union-Find 动态加点 + count ± 1
##### ! 时间复杂度: O(k · α(mn))，k = len(positions)   空间复杂度: O(mn)
##### ! 适用：图在"长"、每一步都要读答案；静态图才用 DFS，动态图就是并查集
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        uf = UnionFind(m * n)  # 格子 (r, c) 编号 r * n + c
        land = [[False] * n for _ in range(m)]
        count = 0
        ans = []
        for r, c in positions:
            if land[r][c]:  # ! 重复加同一格：岛数不变，直接报上一次的数
                ans.append(count)
                continue
            land[r][c] = True
            count += 1  # ! 先当它是一座新岛
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and land[nr][nc]:
                    if uf.union(r * n + c, nr * n + nc):  # ! 和一座已有的岛接上了，少一座
                        count -= 1
            ans.append(count)
        return ans


##################################################################################################
##### ! Solution 2: 每加一格就 DFS 重数一遍（慢速基线，用来对比）
##### ! 时间复杂度: O(k · mn)   空间复杂度: O(mn)
##### ! 适用：只用来理解"为什么动态图不能每次重数"；k 和 mn 都到 1e4 时会超时
##################################################################################################


class Solution_2:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        land = set()
        ans = []
        for r, c in positions:
            land.add((r, c))
            seen = set()
            count = 0
            for cell in land:  # ! 每一步都从头洪水填充：k 次 × O(陆地数)，这就是慢的原因
                if cell in seen:
                    continue
                count += 1
                seen.add(cell)
                stack = [cell]  # 用栈代替递归，陆地最多 1e4 格，链状会爆递归
                while stack:
                    x, y = stack.pop()
                    for nxt in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if nxt in land and nxt not in seen:  # land 里只有合法格子，不用判边界
                            seen.add(nxt)
                            stack.append(nxt)
            ans.append(count)
        return ans


s = Solution_1()
m, n = 3, 3
positions = [[0, 0], [0, 1], [1, 2], [2, 1]]
result = s.numIslands2(m, n, positions)
print(result)  # [1, 1, 2, 3]
print(s.numIslands2(1, 1, [[0, 0]]))  # [1]
