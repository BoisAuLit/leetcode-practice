from typing import List


from collections import deque


class SnakeGame:
    def __init__(self, width: int, height: int, food: List[List[int]]):
        self.i = 0
        self.food = food
        self.deque = deque([(0, 0)])
        self.body = set([(0, 0)])
        self.directions = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
        self.m = height
        self.n = width
        self.score = 0

    def move(self, direction: str) -> int:
        x, y = self.deque[-1]
        dx, dy = self.directions[direction]
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= self.m or ny < 0 or ny >= self.n:
            return -1
        tail = self.deque.popleft()
        self.body.remove(tail)
        if (nx, ny) in self.body:
            return -1
        self.deque.append((nx, ny))
        self.body.add((nx, ny))

        if self.i <= len(self.food) - 1 and (nx, ny) == tuple(
            self.food[self.i]
        ):
            self.deque.appendleft(tail)
            self.body.add(tail)
            self.score += 1
            self.i += 1
        return self.score


# Test case 1: expecting [0, 0, 1, 1, 2, -1]
sg = SnakeGame(3, 2, [[1, 2], [0, 1]])
print(sg.move("R"))
print(sg.move("D"))
print(sg.move("R"))
print(sg.move("U"))
print(sg.move("L"))
print(sg.move("U"))
