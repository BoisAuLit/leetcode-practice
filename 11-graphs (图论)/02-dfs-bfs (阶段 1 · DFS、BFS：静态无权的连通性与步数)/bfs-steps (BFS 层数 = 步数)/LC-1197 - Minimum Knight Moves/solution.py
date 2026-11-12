"""LC-1197 - Minimum Knight Moves

阶段 1 · BFS 层数 = 步数 △ 扩展（会员题）
题目在问：无限棋盘上，马从 (0,0) 跳到 (x,y) 最少几步（题目保证 |x| + |y| <= 300）
点是什么：一个格子 (r, c)   边是什么：马的 8 种跳法
和签名题比改了哪一行：和 1091 一样按层 BFS、层数 = 步数，但棋盘无限，不剪枝会搜爆：
    1) 棋盘四个象限对称，把目标折到第一象限 (|x|, |y|)；
    2) 只在 r, c >= -2 的区域里搜（最短路最多往负方向退两格），搜索面积缩到约 1/4
"""
from collections import deque
from functools import lru_cache

MOVES = ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1))

##################################################################################################
##### ! Solution 1: BFS + 对称剪枝
##### ! 时间复杂度: O(d^2)   空间复杂度: O(d^2)   d = |x| + |y|，搜过的格子数和目标距离的平方同阶
##### ! 适用：最常考的写法；无限图上 BFS，靠对称 + 剪枝把搜索范围压小
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minKnightMoves(self, x: int, y: int) -> int:
        x, y = abs(x), abs(y)  # ! 四个象限对称，目标折到第一象限
        queue = deque([(0, 0)])
        visited = {(0, 0)}
        steps = 0
        while queue:
            for _ in range(len(queue)):
                r, c = queue.popleft()
                if r == x and c == y:
                    return steps
                for dr, dc in MOVES:
                    nr, nc = r + dr, c + dc
                    # ! 剪枝：目标在第一象限，最短路最多往负方向退 2 格，再远就是白走
                    if nr >= -2 and nc >= -2 and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append((nr, nc))
            steps += 1
        return -1  # ! 无限棋盘一定到得了，不会走到这


##################################################################################################
##### ! Solution 2: 双向 BFS
##### ! 时间复杂度: O(d^2) 但常数小很多（两边各搜一半深度）   空间复杂度: O(d^2)
##### ! 适用：起点终点都已知、分支多（8 个方向）时，双向 BFS 把一个大圆换成两个小圆
##################################################################################################


class Solution_2:
    def minKnightMoves(self, x: int, y: int) -> int:
        x, y = abs(x), abs(y)
        if x == 0 and y == 0:
            return 0
        # ! 两边各一张"距离表" + 一个队列；每次只扩较小的那一边
        dist_a, dist_b = {(0, 0): 0}, {(x, y): 0}
        queue_a, queue_b = deque([(0, 0)]), deque([(x, y)])
        while queue_a and queue_b:
            if len(queue_a) > len(queue_b):
                queue_a, queue_b = queue_b, queue_a
                dist_a, dist_b = dist_b, dist_a
            for _ in range(len(queue_a)):  # ! 整层扩完，保证两边各自都是"完整的若干层"
                r, c = queue_a.popleft()
                for dr, dc in MOVES:
                    nr, nc = r + dr, c + dc
                    if nr < -2 or nc < -2 or (nr, nc) in dist_a:
                        continue
                    if (nr, nc) in dist_b:  # ! 碰头：两边的距离拼起来
                        return dist_a[(r, c)] + 1 + dist_b[(nr, nc)]
                    dist_a[(nr, nc)] = dist_a[(r, c)] + 1
                    queue_a.append((nr, nc))
        return -1


##################################################################################################
##### ! Solution 3: 记忆化递归（倒着想最后一步）
##### ! 时间复杂度: O(d^2) 上界，实测远小于 BFS（d = 300 时最多约 4e3 个状态）   空间复杂度: 同状态数
##### !       d = |x| + |y|；递归深度约 d/2（d = 300 时 151 层），默认递归限制够用
##### ! 适用：面试加分项；最后一步一定是从 (r-1, c-2) 或 (r-2, c-1) 跳来，取小的；
##### !       靠近原点时公式会"退过头"，用 base case 兜住
##################################################################################################


class Solution_3:
    def minKnightMoves(self, x: int, y: int) -> int:
        @lru_cache(maxsize=None)
        def dp(r: int, c: int) -> int:
            if r + c == 0:
                return 0  # ! 已在原点
            if r + c == 2:
                return 2  # ! (1,1)/(2,0)/(0,2) 都要 2 步，不能再按公式退
            # ! 最后一步从 (r-1, c-2) 或 (r-2, c-1) 跳来；abs 把退到负半轴的点按对称折回来
            return min(dp(abs(r - 1), abs(c - 2)), dp(abs(r - 2), abs(c - 1))) + 1

        return dp(abs(x), abs(y))


s = Solution_1()
result = s.minKnightMoves(2, 1)
print(result)  # 1

result = s.minKnightMoves(5, 5)
print(result)  # 4
