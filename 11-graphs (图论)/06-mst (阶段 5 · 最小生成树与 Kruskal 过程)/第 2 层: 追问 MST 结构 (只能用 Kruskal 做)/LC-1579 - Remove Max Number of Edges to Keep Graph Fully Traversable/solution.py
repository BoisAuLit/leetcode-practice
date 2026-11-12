"""LC-1579 - Remove Max Number of Edges to Keep Graph Fully Traversable

阶段 5 · 最小生成树与 Kruskal 过程 · 第 2 层: 追问 MST 结构 (只能用 Kruskal 做) ○ 核心
题目在问：边分三种 (1 只 Alice 能走, 2 只 Bob 能走, 3 两人都能走), 最多删几条边, 两人仍各自能走遍全图; 做不到返回 -1
点是什么：n 个点 (编号 1..n)   边是什么：[type, u, v], 类型 3 的边一个人干两个人的活
和签名题比改了哪一行：1584 的 Kruskal 把"按价格排序"换成"按类型审 (3 先, 再 1、2)", 并查集开两个 (Alice / Bob 各一个);
                     union 失败 (成圈) 的边就是多余的, 数一下有几条; 本质是 Kruskal 的"拒绝成圈边"数了两遍
"""
from typing import List


class UnionFind:  # 路径减半 + 按 size 合并, 和 1135 / 1584 一样
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
##### ! Solution 1: 两个并查集, 类型 3 先审, 数"被拒绝"的边
##### ! 时间复杂度: O(E · α(n))   空间复杂度: O(n)
##### ! 适用：问"最多删几条 / 哪些边可有可无"的 MST 结构题; 两个人 = 两个并查集
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxNumEdgesToRemove(self, n: int, edges: List[List[int]]) -> int:
        # ! 为什么类型 3 必须先审 (交换论证):
        # ! 设类型 3 的边最多能不成圈地留 r 条 (类型 3 的生成森林). 任何合法方案里, 留下的类型 3 边
        # ! 做了 k <= r 次有效合并, 那 Alice 至少还要 n-1-k 条类型 1, Bob 至少还要 n-1-k 条类型 2,
        # ! 总共至少留 k + 2(n-1-k) = 2(n-1) - k >= 2(n-1) - r 条. 先审类型 3 恰好取到 k = r, 留得最少.
        # ! 直观: 多留一条不成圈的类型 3 边, 能让 Alice 和 Bob 各省一条自己的边, 净赚一条.
        alice, bob = UnionFind(n + 1), UnionFind(n + 1)  # 编号 1..n, 多开一格
        removed = 0

        # ! 第一轮只审类型 3: 两个并查集都试着 union
        # ! 两边都失败 = 两人都早已连通这两点 = 这条边对谁都没用 -> 可删
        # ! 只要有一边成功就要留着 (哪怕另一边失败)
        for t, u, v in edges:
            if t == 3:
                ok_a = alice.union(u, v)  # 两个 union 都要真的执行, 不能写 a or b (会短路)
                ok_b = bob.union(u, v)
                if not ok_a and not ok_b:
                    removed += 1

        # ! 第二轮: 类型 1 只进 Alice, 类型 2 只进 Bob, union 失败就是多余
        for t, u, v in edges:
            if t == 1 and not alice.union(u, v):
                removed += 1
            elif t == 2 and not bob.union(u, v):
                removed += 1

        # ! 最后两个并查集都必须只剩一派 (1 号所在派的 size == n), 否则有人走不遍
        if alice.size[alice.find(1)] != n or bob.size[bob.find(1)] != n:
            return -1
        return removed


##################################################################################################
##### ! Solution 2: 按类型排序后一趟 Kruskal, 数"留下"的边
##### ! 时间复杂度: O(E log E + E · α(n))   空间复杂度: O(n)
##### ! 适用：想把它写成和 1584 一模一样的"排序 + 一个循环"时; 答案 = 总边数 - 留下的边
##################################################################################################


class Solution_2:
    def maxNumEdgesToRemove(self, n: int, edges: List[List[int]]) -> int:
        alice, bob = UnionFind(n + 1), UnionFind(n + 1)
        kept_a = kept_b = kept = 0  # Alice 树里几条 / Bob 树里几条 / 一共留了几条
        for t, u, v in sorted(edges, key=lambda e: -e[0]):  # ! 类型 3 排最前, 这就是 Kruskal 的"排序"
            if t == 3:
                ok_a = alice.union(u, v)
                ok_b = bob.union(u, v)
                kept_a += ok_a
                kept_b += ok_b
                kept += ok_a or ok_b  # 有一边用上就得留
            elif t == 1:
                ok = alice.union(u, v)
                kept_a += ok
                kept += ok
            else:
                ok = bob.union(u, v)
                kept_b += ok
                kept += ok
        if kept_a != n - 1 or kept_b != n - 1:  # ! 各自恰好 n-1 条有效边 = 各自是一棵生成树
            return -1
        return len(edges) - kept


s = Solution_1()
n = 4
edges = [[3, 1, 2], [3, 2, 3], [1, 1, 3], [1, 2, 4], [1, 1, 2], [2, 3, 4]]
result = s.maxNumEdgesToRemove(n, edges)
print(result)  # 2
