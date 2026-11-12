"""LC-0841 - Keys and Rooms

阶段 0 · 建图、隐式图、状态图 · 显式建图(边列表 → 邻接表) ○ 核心
题目在问：从 0 号房间出发，捡到的钥匙能不能把所有房间都打开
点是什么：房间 0..n-1   边是什么：房间 i 里的钥匙 j 就是有向边 i → j(rooms 本身已经是邻接表，不用建图)
和签名题(1971)比改了哪一行：无向 → 有向，建图那两行 graph[a].append(b) / graph[b].append(a) 删掉，直接用 rooms[i]；
  判定从 "到没到 destination" 变成 "len(visited) == n"
"""
from typing import List
from collections import deque


##################################################################################################
##### ! Solution 1: DFS 迭代(栈)(用户原版，class 名为 Solution_DFS_Using_Stack)
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V)   V = 房间数，E = 钥匙总数；每把钥匙看一次
##### ! 适用：有向图可达性的默认写法；rooms 就是邻接表，省掉建图
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution   (用户实测最快；和 BFS 逻辑完全一样，只是 pop 的方向)
##################################################################################################
# ! This one is a lot significantly faster the the BFS solution
class Solution_DFS_Using_Stack:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        stack = deque([0])
        visited = set([0])
        while stack:
            index = stack.pop()
            for room in rooms[index]:
                if room not in visited:
                    visited.add(room)
                    stack.append(room)
        return len(visited) == len(rooms)
        


##################################################################################################
##### ! Solution 2: BFS 队列(用户原版，class 名为 Solution_BFS_Using_Queue)
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V)
##### ! 适用：和栈版只差 popleft；"超慢" 是因为循环里留了一行 print(index) 调试输出(n 到 1000 时打印很贵)，去掉后和 DFS 一样快
##################################################################################################
# ! This one is super slow
class Solution_BFS_Using_Queue:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        queue = deque([0])
        visited = set([0])
        while queue:
            index = queue.popleft()
            print(index)
            for room in rooms[index]:
                if room not in visited:
                    visited.add(room)
                    queue.append(room)
        return len(visited) == len(rooms)


##################################################################################################
##### ! Solution 3: DFS 递归
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V)   递归栈最深 V 层；n ≤ 1000 不会爆 Python 默认深度
##### ! 适用：最短写法；注意 visited 要在 "进房间" 时标，不要在 "拿到钥匙" 时标，两种都对但别混用
##################################################################################################


class Solution_3:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        visited = set()

        def dfs(room: int) -> None:
            visited.add(room)  # ! 进了这个房间
            for key in rooms[room]:
                if key not in visited:
                    dfs(key)  # ! 没去过的房间，拿钥匙直接进

        dfs(0)
        return len(visited) == len(rooms)



# s = Solution()

# # Test case 1: Expecting True
# # input_ = [[1], [2], [3], []]

# # Test case 2: Expecting False
# input_ = [[1,3],[3,0,1],[2],[0]]

# result = s.canVisitAllRooms(input_)
# print(result)

s = Solution_DFS_Using_Stack()
rooms = [[1, 3], [3, 0, 1], [2], [0]]
result = s.canVisitAllRooms(rooms)
print(result)  # False (2 号房间的钥匙锁在 2 号房间里)
