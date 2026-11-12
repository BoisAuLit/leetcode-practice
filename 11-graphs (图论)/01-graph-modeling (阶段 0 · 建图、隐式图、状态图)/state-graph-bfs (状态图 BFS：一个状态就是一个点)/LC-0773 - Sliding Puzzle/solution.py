"""LC-0773 - Sliding Puzzle

阶段 0 · 状态图 BFS △ 扩展
题目在问：2x3 滑块拼图最少几步复原成 [[1,2,3],[4,5,0]]，复原不了返回 -1
点是什么：整个棋盘按行拼成的 6 位串(如 "123450")   边是什么：0 和上下左右某个数字交换位置
和签名题比改了哪一行：752 的点是 4 位密码串、邻居是拨一位；
    本题的点是整个棋盘序列化成的串，邻居由"0 在哪个下标"决定，查一张 6 行的邻居表。
    状态总数 6! = 720，BFS 随便跑；一半状态(奇偶性不对)永远到不了，BFS 跑空返回 -1。
"""
from collections import deque
from heapq import heappush, heappop
from typing import List

# ! 棋盘按行拉平后下标 0..5 对应 [[0,1,2],[3,4,5]]，表里是每个下标的上下左右邻居
NEIGHBORS = [
    [1, 3],
    [0, 2, 4],
    [1, 5],
    [0, 4],
    [1, 3, 5],
    [2, 4],
]
TARGET = "123450"


def swap(state: str, i: int, j: int) -> str:
    s = list(state)
    s[i], s[j] = s[j], s[i]
    return "".join(s)


##################################################################################################
##### ! Solution 1: BFS，状态 = 6 位串，邻居查表
##### ! 时间复杂度: O(6! · 3) = O(1)   空间复杂度: O(6!)
##### ! 适用：无权最短步数的标准写法，状态图 BFS 模板本身
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def slidingPuzzle(self, board: List[List[int]]) -> int:
        start = "".join(str(x) for row in board for x in row)  # ! 序列化：棋盘 → 6 位串
        if start == TARGET:
            return 0

        queue = deque([(start, 0)])
        visited = {start}
        while queue:
            state, steps = queue.popleft()
            z = state.index("0")  # ! 0 在哪，决定能和谁交换
            for nb in NEIGHBORS[z]:
                nxt = swap(state, z, nb)  # ! 交换 = 走一条边
                if nxt == TARGET:
                    return steps + 1
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, steps + 1))
        return -1


##################################################################################################
##### ! Solution 2: A*，启发值 = 每块数字离目标格的曼哈顿距离之和
##### ! 时间复杂度: O(6! · log 6!) 最坏   空间复杂度: O(6!)
##### ! 适用：状态空间大(3x3 八数码、4x4 十五数码)时比 BFS 少探很多；本题纯练手
##################################################################################################


def manhattan(state: str) -> int:
    h = 0
    for idx, ch in enumerate(state):
        if ch == "0":
            continue
        goal = int(ch) - 1  # ! 数字 k 应该在下标 k-1
        h += abs(idx // 3 - goal // 3) + abs(idx % 3 - goal % 3)
    return h


class Solution_2:
    def slidingPuzzle(self, board: List[List[int]]) -> int:
        start = "".join(str(x) for row in board for x in row)
        heap = [(manhattan(start), 0, start)]  # (f = g + h, g = 已走步数, 状态)
        best = {start: 0}  # ! 每个状态目前已知的最短 g
        while heap:
            _, g, state = heappop(heap)
            if state == TARGET:
                return g  # ! 启发值不超估(每步只能让一块数字移 1 格)，第一次弹出目标就是最优
            if g > best[state]:  # 作废票
                continue
            z = state.index("0")
            for nb in NEIGHBORS[z]:
                nxt = swap(state, z, nb)
                if nxt not in best or g + 1 < best[nxt]:
                    best[nxt] = g + 1
                    heappush(heap, (g + 1 + manhattan(nxt), g + 1, nxt))
        return -1


s = Solution_1()
board = [[4, 1, 2], [5, 0, 3]]
result = s.slidingPuzzle(board)
print(result)  # 5
