"""LC-0909 - Snakes and Ladders

阶段 0 · 状态图 BFS △ 扩展
题目在问：蛇梯棋从 1 号格到 n*n 号格最少掷几次骰子，到不了返回 -1
点是什么：格子编号 1..n*n   边是什么：掷骰子走 +1..+6，落点有蛇/梯就被强制传送(每次只传一次)
和签名题比改了哪一行：752 的邻居是拨一位；本题的邻居是 curr+1..curr+6 再查一次 board。
    唯一的坑是 board 用二维"牛耕式"(boustrophedon)编号：从左下角开始，一行向右、一行向左，
    所以要写一个 编号 → (row, col) 的换算，其余和 BFS 模板一样。
"""
from collections import deque
from typing import List


def to_cell(s: int, n: int) -> tuple:
    # ! 编号 s (1..n*n) → (row, col)
    # 画面：s-1 除以 n，商 q = 从底往上数第几行(0 起)，余数 r = 这一行里第几个(0 起)
    #   q 偶数：这一行从左往右，col = r
    #   q 奇数：这一行从右往左，col = n-1-r
    #   行号要上下翻：底行是 board[n-1]，所以 row = n-1-q
    q, r = divmod(s - 1, n)
    row = n - 1 - q
    col = r if q % 2 == 0 else n - 1 - r
    return row, col


##################################################################################################
##### ! Solution 1: BFS + visited 集合
##### ! 时间复杂度: O(n^2 · 6)   空间复杂度: O(n^2)
##### ! 适用：无权最短步数的标准写法；状态就是编号，没有二维状态
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        n = len(board)
        target = n * n
        queue = deque([(1, 0)])  # (当前格, 已掷次数)
        visited = {1}
        while queue:
            curr, rolls = queue.popleft()
            for nxt in range(curr + 1, min(curr + 6, target) + 1):  # ! 骰子 1..6，不能越过 n*n
                r, c = to_cell(nxt, n)
                if board[r][c] != -1:
                    nxt = board[r][c]  # ! 被蛇/梯传送，只传一次，落点上再有蛇梯也不跟
                if nxt == target:
                    return rolls + 1
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, rolls + 1))
        return -1


##################################################################################################
##### ! Solution 2: BFS + dist 数组(-1 表示没到过)，换算内联
##### ! 时间复杂度: O(n^2 · 6)   空间复杂度: O(n^2)
##### ! 适用：想顺便拿到每个格子的最少次数时；数组比 set 常数小
##################################################################################################


class Solution_2:
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        n = len(board)
        target = n * n
        dist = [-1] * (target + 1)  # ! 下标 = 编号，0 号闲置
        dist[1] = 0
        queue = deque([1])
        while queue:
            curr = queue.popleft()
            if curr == target:
                return dist[curr]
            for nxt in range(curr + 1, min(curr + 6, target) + 1):
                q, r = divmod(nxt - 1, n)  # ! 同 to_cell，内联写一遍
                row = n - 1 - q
                col = r if q % 2 == 0 else n - 1 - r
                if board[row][col] != -1:
                    nxt = board[row][col]
                if dist[nxt] == -1:
                    dist[nxt] = dist[curr] + 1
                    queue.append(nxt)
        return -1


s = Solution_1()
board = [
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, 35, -1, -1, 13, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, 15, -1, -1, -1, -1],
]
result = s.snakesAndLadders(board)
print(result)  # 4
