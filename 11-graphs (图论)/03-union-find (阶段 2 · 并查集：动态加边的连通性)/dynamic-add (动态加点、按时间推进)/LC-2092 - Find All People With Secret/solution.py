"""LC-2092 - Find All People With Secret

阶段 2 · 并查集动态加点 (按时间推进) △ 扩展
题目在问：n 个人、会议 [x, y, time]；0 号在 time 0 把秘密告诉 firstPerson，会议里秘密瞬时传播，最后谁知道
点是什么：人   边是什么：会议，但边是"限时"的：只在它那个时刻有效，过了就作废
和签名题比改了哪一行：1101 是按时间排序后一路 union，边永远有效；这里同一时刻的会议一起 union，
                      这一时刻处理完后，没和 0 同派的人要"重置" (parent[x] = x)，不让这条边留到下一时刻
"""
from collections import defaultdict, deque
from heapq import heappop, heappush
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
##### ! Solution 1: Union-Find + 按时刻分组 + 重置
##### ! 时间复杂度: O(m log m + (n + m) · α(n))   空间复杂度: O(n)
##### ! 适用：手册点名的进阶用法；"同一时刻瞬时传播"正好是"一组边一起 union"，不知道秘密的人事后拆开
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findAllPeople(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        uf = UnionFind(n)
        uf.union(0, firstPerson)  # time 0 的那次"会议"
        meetings.sort(key=lambda mt: mt[2])

        i, m = 0, len(meetings)
        while i < m:
            j = i
            while j < m and meetings[j][2] == meetings[i][2]:  # [i, j) 是同一时刻的一组
                j += 1
            for x, y, _ in meetings[i:j]:  # ! 先把这一组全部 union：秘密在这一刻瞬时传遍整派
                uf.union(x, y)
            for x, y, _ in meetings[i:j]:  # ! 再检查：没和 0 同派的，这一刻白聊了，拆成单人
                for p in (x, y):
                    if uf.find(p) != uf.find(0):
                        uf.parent[p] = p  # 重置；不知道秘密的人此刻只和"这一组"的人连着，一个个拆干净
                        uf.size[p] = 1
            i = j

        root = uf.find(0)
        return [p for p in range(n) if uf.find(p) == root]


##################################################################################################
##### ! Solution 2: Dijkstra by time (每个人最早几点知道)
##### ! 时间复杂度: O((n + m) log m)   空间复杂度: O(n + m)
##### ! 适用：把"知道秘密的时间"当距离：只能走开会时间 >= 我知道时间的边，最早时间优先出堆
##################################################################################################


class Solution_2:
    def findAllPeople(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        adj = defaultdict(list)
        for x, y, t in meetings:
            adj[x].append((y, t))
            adj[y].append((x, t))

        INF = float("inf")
        earliest = [INF] * n  # 每个人最早几点知道秘密
        earliest[0] = earliest[firstPerson] = 0
        heap = [(0, 0), (0, firstPerson)]
        while heap:
            t, u = heappop(heap)
            if t > earliest[u]:  # 作废票
                continue
            for v, tm in adj[u]:
                # ! 只能走"开会时间 >= 我知道秘密的时间"的边 (取等号：同一时刻瞬时传播)
                if tm >= t and tm < earliest[v]:
                    earliest[v] = tm
                    heappush(heap, (tm, v))
        return [p for p in range(n) if earliest[p] < INF]


##################################################################################################
##### ! Solution 3: 按时刻分组 + 组内 BFS
##### ! 时间复杂度: O(m log m + n + m)   空间复杂度: O(n + m)
##### ! 适用：每个时刻单独建一张小图，从已知道秘密的人出发 BFS，碰到的全知道；小图用完即弃，天然不用"重置"
##################################################################################################


class Solution_3:
    def findAllPeople(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        knows = [False] * n
        knows[0] = knows[firstPerson] = True
        meetings.sort(key=lambda mt: mt[2])

        i, m = 0, len(meetings)
        while i < m:
            j = i
            while j < m and meetings[j][2] == meetings[i][2]:
                j += 1
            adj = defaultdict(list)  # 这一时刻的小图
            for x, y, _ in meetings[i:j]:
                adj[x].append(y)
                adj[y].append(x)
            q = deque(p for p in adj if knows[p])  # ! 种子：这一刻开会的人里已经知道秘密的
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if not knows[v]:
                        knows[v] = True
                        q.append(v)
            i = j
        return [p for p in range(n) if knows[p]]


s = Solution_1()
n = 6
meetings = [[1, 2, 5], [2, 3, 8], [1, 5, 10]]
firstPerson = 1
result = s.findAllPeople(n, meetings, firstPerson)
print(result)  # [0, 1, 2, 3, 5]
print(Solution_1().findAllPeople(4, [[3, 1, 3], [1, 2, 2], [0, 3, 3]], 3))  # [0, 1, 3]
print(Solution_1().findAllPeople(5, [[3, 4, 2], [1, 2, 1], [2, 3, 1]], 1))  # [0, 1, 2, 3, 4]
