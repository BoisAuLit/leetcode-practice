"""LC-0323 - Number of Connected Components in an Undirected Graph

合并自 3 个解法文件:
  1. 0323 - A - Number of Connected Components - Union-Find.py
  2. 0323 - B - Number of Connected Components - DFS.py
  3. 0323 - C - Number of Connected Components - BFS.py

阶段 2 · 并查集计数 ★ 签名题
题目在问：n 个点 + 边列表，一共有几个连通块
点是什么：0..n-1 的编号   边是什么：edges 里的无向边，一条条加进来
和签名题比改了哪一行：本题就是签名题（块数 = n − 成功合并次数）
"""

from typing import List

from collections import defaultdict

from collections import deque, defaultdict


# ============================================================================
# Solution 1: Union_Find    (原文件: 0323 - A - Number of Connected Components - Union-Find.py)
# ============================================================================

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

    def getCount(self):
        return self.count

    def isConnected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

##################################################################################################
##### ! Solution 1: Union-Find（UF 内部维护 count，每次成功合并 count -= 1）
##### ! 时间复杂度: O((n + E) · α(n))   空间复杂度: O(n)
##### ! 适用：动态加边、只问块数；和 Solution 4 完全等价，只是把计数藏进了 UF 里
##################################################################################################

class Solution_1_Union_Find:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        uf = UnionFind(n)
        for x, y in edges:
            uf.union(x, y)
        return uf.getCount()

# ============================================================================
# Solution 2: DFS    (原文件: 0323 - B - Number of Connected Components - DFS.py)
# ============================================================================

n_2 = 5

edges_2 = [[0, 1], [1, 2], [3, 4]]

##################################################################################################
##### ! Solution 2: DFS（迭代栈；从未访问集合里随便挑一个起点，走完一块 res += 1）
##### ! 时间复杂度: O(n + E)   空间复杂度: O(n + E)
##### ! 适用：静态图（边一次给全）、顺便要拿到每块的点；没有动态加边时 DFS 和并查集一样好
##################################################################################################

class Solution_2_DFS:
    def countComponents(self, n_2: int, edges_2: List[List[int]]) -> int:
        adj = defaultdict(list)

        for a, b in edges_2:
            adj[a].append(b)
            adj[b].append(a)

        nodes = set(range(n_2))  # 所有还没访问过的节点
        res = 0

        while nodes:
            node = nodes.pop()  # 随便选一个未访问节点
            stack = [node]

            while stack:
                node = stack.pop()

                for neigh in adj[node]:
                    if neigh in nodes:
                        nodes.remove(neigh)
                        stack.append(neigh)

            res += 1

        return res

# ============================================================================
# Solution 3: BFS    (原文件: 0323 - C - Number of Connected Components - BFS.py)
# ============================================================================

n_3 = 5

edges_3 = [[0, 1], [1, 2], [3, 4]]

##################################################################################################
##### ! Solution 3: BFS（和 Solution 2 只差 stack → deque）
##### ! 时间复杂度: O(n + E)   空间复杂度: O(n + E)
##### ! 适用：同 DFS，两种写法二选一即可
##################################################################################################

class Solution_3_BFS:
    def countComponents(self, n_3: int, edges_3: List[List[int]]) -> int:
        adj = defaultdict(list)

        for a, b in edges_3:
            adj[a].append(b)
            adj[b].append(a)

        nodes = set(range(n_3))  # 所有还没访问过的节点
        res = 0

        while nodes:  # 随便选一个未访问节点
            node = nodes.pop()
            q = deque([node])

            while q:
                node = q.popleft()

                for neigh in adj[node]:
                    if neigh in nodes:
                        nodes.remove(neigh)
                        q.append(neigh)

            res += 1

        return res


##################################################################################################
##### ! Solution 4: Union-Find，union 返回 bool（手册签名写法：块数 = n − 成功合并次数）
##### ! 时间复杂度: O((n + E) · α(n))   空间复杂度: O(n)
##### ! 适用：动态加边、只问块数/是否同派；union 的返回值在 684（成环）、1319、1101 里反复复用
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution（和 Solution 1 等价，但"成功合并才减一"这个动作是本阶段的出关标准）
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


class Solution_4:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        uf = UnionFindBool(n)
        count = n  # ! 一开始每个点各自一派
        for a, b in edges:
            if uf.union(a, b):  # ! 只有真的把两派合成一派时才减一
                count -= 1
        return count


if __name__ == "__main__":

    # --- Solution 2: DFS ---
    s = Solution_2_DFS()
    result = s.countComponents(n_2, edges_2)
    print(result)

    # --- Solution 3: BFS ---
    s = Solution_3_BFS()
    result = s.countComponents(n_3, edges_3)
    print(result)


if __name__ == "__main__":

    # --- Solution 4: Union-Find, union 返回 bool (Preferred) ---
    s = Solution_4()
    n = 5
    edges = [[0, 1], [1, 2], [3, 4]]
    result = s.countComponents(n, edges)
    print(result)  # 2
    result = s.countComponents(5, [[0, 1], [1, 2], [2, 3], [3, 4]])
    print(result)  # 1
