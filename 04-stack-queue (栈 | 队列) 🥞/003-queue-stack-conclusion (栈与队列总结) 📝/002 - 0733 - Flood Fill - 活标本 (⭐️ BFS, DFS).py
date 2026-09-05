from typing import List
from collections import deque


# ! Approach 1: DFS using recursion
class Solution_DFS_With_Recursion:
    def floodFill(
        self, image: List[List[int]], sr: int, sc: int, color: int
    ) -> List[List[int]]:
        original_color = image[sr][sc]
        visited = set() # Here visited doesn't contain the initial point
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        m = len(image)
        n = len(image[0])

        def dfs(x: int, y: int):
            if not (
                0 <= x < m
                and 0 <= y < n
                and (x, y) not in visited
                and image[x][y] == original_color
            ):
                return
            visited.add((x, y)) # We set the visited here
            image[x][y] = color
            for dx, dy in directions:
                x1, y1 = x + dx, y + dy
                dfs(x1, y1)

        dfs(sr, sc)
        return image


# ! Approach 2: DFS using stack
# ! [x, x, x, x, x, x] <-- Push(), Pop()
class Solution_DFS_Using_Stack:
    def floodFill(
        self, image: List[List[int]], sr: int, sc: int, color: int
    ) -> List[List[int]]:
        visited = set([(sr, sc)]) # Here visisted contains the starting point
        stack = deque([(sr, sc)]) # Here we initialize the stack with the starting point
        original_color = image[sr][sc]
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        m = len(image)
        n = len(image[0])
        while stack:
            # ! This is actually the Pop() operation
            x, y = stack.pop()
            image[x][y] = color
            for dx, dy in directions:
                x1, y1 = x + dx, y + dy
                if (
                    0 <= x1 < m
                    and 0 <= y1 < n
                    and (x1, y1) not in visited
                    and image[x1][y1] == original_color
                ):
                    # ! This is actually the Push() operation
                    stack.append((x1, y1))
                    visited.add((x1, y1)) # We add visited here
        return image


# ! Appraoch 3: BFS using queue
# ! Head / Deque() --> [x, x, x, x, x, x] <-- Tail / Enqueue()
class Solution_BFS_Using_Queue:
    def floodFill(
        self, image: List[List[int]], sr: int, sc: int, color: int
    ) -> List[List[int]]:
        visited = set([(sr, sc)]) # Here visited contains the starting point
        queue = deque([(sr, sc)]) # We initialize the queue with the startig point
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        original_color = image[sr][sc]
        m = len(image)
        n = len(image[0])
        while queue:
            # ! This is actually the Deque() operation (Happening on Head)
            x, y = queue.popleft() 
            image[x][y] = color
            for dx, dy in directions:
                x1, y1 = x + dx, y + dy
                if (
                    0 <= x1 < m
                    and 0 <= y1 < n
                    and (x1, y1) not in visited
                    and image[x1][y1] == original_color
                ):
                    # ! This is actually the Enque() operation (happening at Tail)
                    queue.append((x1, y1))
                    visited.add((x1, y1)) # We add visited here
        return image
