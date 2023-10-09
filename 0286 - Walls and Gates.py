from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        queue = []
        m = len(rooms)
        n = len(rooms[0])
        nbRooms = 0
        for x in range(m):
            for y in range(n):
                if rooms[x][y] == 0:
                    queue.append((x, y))
                elif rooms[x][y] == 2147483647:
                    nbRooms += 1
        if not queue:
            return
        distance = 1
        roomsCount = 0
        while queue:
            newQueue = []
            for x, y in queue:
                for newX, newY in [
                    (x + 1, y),
                    (x - 1, y),
                    (x, y + 1),
                    (x, y - 1),
                ]:
                    if 0 <= newX < m and 0 <= newY < n:
                        if rooms[newX][newY] == 2147483647:
                            rooms[newX][newY] = distance
                            newQueue.append((newX, newY))
                            roomsCount += 1
            if roomsCount == nbRooms:
                break
            queue = newQueue
            distance += 1


s = Solution()
# input_ = [
#     [2147483647, -1, 0, 2147483647],
#     [2147483647, 2147483647, 2147483647, -1],
#     [2147483647, -1, 2147483647, -1],
#     [0, -1, 2147483647, 2147483647],
# ]
# input_ = [[2147483647]]
input_ = [
    [2147483647, 0, 2147483647, 2147483647, 0, 2147483647, -1, 2147483647]
]
result = s.wallsAndGates(input_)
print(input_)

"""

"""
