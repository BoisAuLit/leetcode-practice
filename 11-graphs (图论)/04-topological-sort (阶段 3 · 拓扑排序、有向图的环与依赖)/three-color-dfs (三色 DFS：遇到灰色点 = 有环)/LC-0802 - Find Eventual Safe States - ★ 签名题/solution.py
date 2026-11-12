"""LC-0802 - Find Eventual Safe States

阶段 3 · 三色 DFS（遇到灰色点 = 有环） ★ 签名题
题目在问：有向图里从哪些点出发，不管怎么走最后都停在"终点"（出度 0 的点），永远走不进环
点是什么：下标 0..n-1   边是什么：graph[u] 里的每个 v 是一条 u -> v
和签名题比改了哪一行：本题就是签名题。白 = 没来过、灰 = 还在递归栈上、黑 = 已确认安全；
                     DFS 碰到灰点 = 走回了自己来的路 = 有环；只有所有出边都安全的点才能染黑
"""
import sys
from collections import deque
from typing import List

sys.setrecursionlimit(20000)  # ! n 到 1e4，一条链的递归深度就是 n，默认 1000 会爆；怕递归就用 Solution 3

##################################################################################################
##### ! Solution 1: 三色 DFS（递归）
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V)（颜色数组 + 递归栈）
##### ! 适用：问"从哪些点出发走不进环"、"从 u 出发是否一定能到终点"；签名写法，面试先写这个
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        n = len(graph)
        WHITE, GRAY, BLACK = 0, 1, 2
        color = [WHITE] * n

        def safe(u: int) -> bool:
            if color[u] != WHITE:
                return color[u] == BLACK  # ! 灰 = 正在栈上，或上次没走通留下的灰，都是不安全
            color[u] = GRAY
            for v in graph[u]:
                if not safe(v):
                    return False  # ! 有一条出边不安全 u 就不安全；故意留灰，下次碰到直接判不安全
            color[u] = BLACK  # 所有出边都安全，u 才安全
            return True

        return [u for u in range(n) if safe(u)]


##################################################################################################
##### ! Solution 2: 反图 + Kahn（按出度剥）
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V + E)（反图）
##### ! 适用：不想递归时；画面：把边全部反向，终点变成入度 0 的点，能被 Kahn 出队的点就是安全点
##################################################################################################


class Solution_2:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        n = len(graph)
        rev = [[] for _ in range(n)]
        outdeg = [len(graph[u]) for u in range(n)]  # ! 原图出度 = 反图入度
        for u in range(n):
            for v in graph[u]:
                rev[v].append(u)

        q = deque(u for u in range(n) if outdeg[u] == 0)  # 终点先进队
        safe = [False] * n
        while q:
            v = q.popleft()
            safe[v] = True
            for u in rev[v]:  # 指向 v 的点，少了一条"可能走进环"的出边
                outdeg[u] -= 1
                if outdeg[u] == 0:  # ! 所有出边都通向安全点，u 安全
                    q.append(u)
        return [u for u in range(n) if safe[u]]


##################################################################################################
##### ! Solution 3: 三色 DFS（迭代，显式栈）
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V)
##### ! 适用：和 Solution 1 同一套三色逻辑，只是把递归栈换成 (点, 下一条出边下标) 的手写栈，n 再大也不怕
##################################################################################################


class Solution_3:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        n = len(graph)
        WHITE, GRAY, BLACK = 0, 1, 2
        color = [WHITE] * n

        for s in range(n):
            if color[s] != WHITE:
                continue
            color[s] = GRAY
            stack = [(s, 0)]  # (点, 下一条要看的出边下标)
            while stack:
                u, i = stack[-1]
                if i == len(graph[u]):  # 出边看完了，没有一条不安全（否则早就清栈了）
                    color[u] = BLACK
                    stack.pop()
                    continue
                stack[-1] = (u, i + 1)
                v = graph[u][i]
                if color[v] == WHITE:
                    color[v] = GRAY
                    stack.append((v, 0))
                elif color[v] == GRAY:
                    stack.clear()  # ! 踩到灰点：栈上每个点都能走到 v，全部不安全，留灰直接清栈

        return [u for u in range(n) if color[u] == BLACK]


s = Solution_1()
graph = [[1, 2], [2, 3], [5], [0], [5], [], []]
result = s.eventualSafeNodes(graph)
print(result)  # [2, 4, 5, 6]
