from typing import List
from collections import deque


class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        if not rooms:
            return []
        m = len(rooms)
        n = len(rooms[0])
        queue = deque()

        # Find all the doors
        for r in range(m):
            for c in range(n):
                if rooms[r][c] == 0:
                    queue.append((r, c))
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        while queue:
            x, y = queue.popleft()
            distance = rooms[x][y] + 1
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (
                    0 <= new_x < m
                    and 0 <= new_y < n
                    and rooms[new_x][new_y] == 2147483647
                ):
                    rooms[new_x][new_y] = distance
                    queue.append((new_x, new_y))
        return rooms
