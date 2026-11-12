"""LC-0752 - Open the Lock

阶段 0 · 建图、隐式图、状态图 · 状态图 BFS ★ 签名题
题目在问：四位转盘锁从 "0000" 最少转几次到 target，中途不能碰到 deadends；到不了 -1
点是什么：一个四位串(共 10^4 个)   边是什么：拨一位 ±1(每个点 8 个邻居)，无权
和签名题比改了哪一行：本题就是签名题。图不存在内存里，邻居现场算；deadends 相当于 "不能走的点"
"""
from collections import deque


##################################################################################################
##### ! Solution 1: 状态图 BFS，队列里带步数(用户原版，class 名为 Solution)
##### ! 时间复杂度: O(10^4 · 8 · 4) = O(N · 8 · L)   空间复杂度: O(10^4)   N = 状态数，L = 4 位；每个状态进队一次
##### ! 适用：单源无权最短步数的标准模板；邻居不存图、现场拼字符串
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution:
    def openLock(self, deadends: list[str], target: str) -> int:
        dead = set(deadends)
        if "0000" in dead:
            return -1
        if target == "0000":
            return 0
        
        queue = deque([("0000", 0)])
        visited = {"0000"}

        while queue:
            curr, turns = queue.popleft()
            
            if curr == target:
                return turns

            for i in range(4):
                for d in (-1, 1):  # Move up or down
                    new_digit = str((int(curr[i]) + d) % 10)
                    new_combo = curr[:i] + new_digit + curr[i+1:]

                    if new_combo not in visited and new_combo not in dead:
                        visited.add(new_combo)
                        queue.append((new_combo, turns + 1))

        return -1  # If no path found




##################################################################################################
##### ! Solution 2: 分层 BFS，deadends 直接塞进 visited
##### ! 时间复杂度: O(10^4 · 8 · 4)   空间复杂度: O(10^4)   同 Solution 1
##### ! 适用：同一模板的另一种画面：visited 初始化成 set(deadends)，就不用在循环里单独判 dead；按层数步数
##################################################################################################


class Solution_2:
    def openLock(self, deadends: list[str], target: str) -> int:
        visited = set(deadends)  # ! 死锁状态 = 一开始就 "走过了"，自然不会再进队
        if "0000" in visited:
            return -1
        visited.add("0000")
        queue = deque(["0000"])
        step = 0
        while queue:
            for _ in range(len(queue)):  # ! 一层一层剥，剥完一层 step + 1
                curr = queue.popleft()
                if curr == target:
                    return step
                for i in range(4):
                    for d in (-1, 1):
                        nxt = curr[:i] + str((int(curr[i]) + d) % 10) + curr[i + 1:]
                        if nxt not in visited:
                            visited.add(nxt)
                            queue.append(nxt)
            step += 1
        return -1


##################################################################################################
##### ! Solution 3: 双向 BFS
##### ! 时间复杂度: O(10^4 · 8 · 4) 最坏，实际约两个半径一半的球，常数小很多   空间复杂度: O(10^4)
##### ! 适用：起点终点都已知、分支多(每点 8 个邻居)时；每次扩展人少的那一头，两头的 visited 一碰上就是答案
##################################################################################################


class Solution_3:
    def openLock(self, deadends: list[str], target: str) -> int:
        dead = set(deadends)
        if "0000" in dead or target in dead:
            return -1
        if target == "0000":
            return 0
        front, back = {"0000"}, {target}  # ! 两头各自的当前层
        seen = {"0000", target}
        step = 0
        while front and back:
            if len(front) > len(back):  # ! 永远扩展小的那一头
                front, back = back, front
            step += 1
            nxt_layer = set()
            for curr in front:
                for i in range(4):
                    for d in (-1, 1):
                        nxt = curr[:i] + str((int(curr[i]) + d) % 10) + curr[i + 1:]
                        if nxt in back:
                            return step  # ! 两头相遇
                        if nxt not in seen and nxt not in dead:
                            seen.add(nxt)
                            nxt_layer.add(nxt)
            front = nxt_layer
        return -1


s = Solution()

# Test case 1: Expecting 6
# deadends = ["0201", "0101", "0102", "1212", "2002"]
# target = "0202"

# Test case 2: Expecting 1
# deadends = ["8888"]
# target = "0009"

# Test case 3: Expecting -1
deadends = ["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"]
target = "8888"

# Test case 4: Expecting -1 (when deadends contains "0000")
deadends = ["0000"]
target = "1111"

# Test case 5: Expecting -1 (when deadends doesn't contain "0000" and target is "0000")
deadends = ["1587"]
target = "0000"

result = s.openLock(deadends, target)
print(result)
