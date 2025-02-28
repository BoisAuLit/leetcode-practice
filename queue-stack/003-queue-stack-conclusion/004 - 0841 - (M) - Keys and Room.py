from typing import List
from collections import deque


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


# s = Solution()

# # Test case 1: Expecting True
# # input_ = [[1], [2], [3], []]

# # Test case 2: Expecting False
# input_ = [[1,3],[3,0,1],[2],[0]]

# result = s.canVisitAllRooms(input_)
# print(result)
