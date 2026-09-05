from typing import List
import heapq


class TaskManager:
    def __init__(self, tasks: List[List[int]]):
        self.heap = list()
        self.hashtable = dict()
        self.removed = set()
        for user, taskId, priority in tasks:
            heapq.heappush(self.heap, (-priority, -taskId))
            self.hashtable[taskId] = [user, priority]

    def add(self, userId: int, taskId: int, priority: int) -> None:
        if taskId in self.removed:
            self.removed.remove(taskId)
        heapq.heappush(self.heap, (-priority, -taskId))
        self.hashtable[taskId] = [userId, priority]

    def edit(self, taskId: int, newPriority: int) -> None:
        self.hashtable[taskId][1] = newPriority
        heapq.heappush(self.heap, (-newPriority, -taskId))

    def rmv(self, taskId: int) -> None:
        self.removed.add(taskId)

    def execTop(self) -> int:
        while self.heap:
            entry = heapq.heappop(self.heap)
            priority, taskId = -entry[0], -entry[1]
            # Must not be removed previously
            if taskId in self.removed:
                continue
            # Must not be a stale record
            if self.hashtable[taskId][1] != priority:
                continue
            self.rmv(taskId)
            return self.hashtable[taskId][0]

        return -1


t = TaskManager([[1, 101, 8], [2, 102, 20], [3, 103, 5]])
print(t.add(4, 104, 5))
print(t.edit(102, 9))
print(t.execTop())
print(t.rmv(101))
print(t.add(0, 101, 8))
print(t.execTop())
