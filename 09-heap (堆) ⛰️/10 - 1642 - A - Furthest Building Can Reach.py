from typing import List
import heapq


class Solution_1:
    """
    Principle: ladders are better,
    however tall the next jump is, we can always use ladders.
    Ladders are precious, we should use all the ladders to climb
    all the highest jumps.

    Firstly, use up all the ladders.

    When the ladders are used up,
    replace the most wasteful ladder (the ladder that climbed the least floor) with bricks.
    When we cannot use bricks anymore, it means that we cannot climb to the next building.
    """

    def furthestBuilding(
        self, heights: List[int], bricks: int, ladders: int
    ) -> int:
        ladder_allocations = []  # We'll use heapq to treat this as a min-heap.
        for i in range(len(heights) - 1):
            climb = heights[i + 1] - heights[i]
            # If this is actually a "jump down", skip it.
            if climb <= 0:
                continue
            # Otherwise, allocate a ladder for this climb.
            heapq.heappush(ladder_allocations, climb)
            # If we haven't gone over the number of ladders, nothing else to do.
            if len(ladder_allocations) <= ladders:
                continue
            # Otherwise, we will need to take a climb out of ladder_allocations
            bricks -= heapq.heappop(ladder_allocations)
            # If this caused bricks to go negative, we can't get to i + 1
            if bricks < 0:
                return i
        # If we got to here, this means we had enough to cover every climb.
        return len(heights) - 1


class Solution_2:
    """
    Principle:
    Use up bricks first. When bricks are used up,
    we start replace the jump with the most bricks with ladders

    """

    def furthestBuilding(
        self, heights: List[int], bricks: int, ladders: int
    ) -> int:
        bricks_allocation = []  # max heap
        for i in range(len(heights) - 1):
            climb = heights[i + 1] - heights[i]

            # If this is actually a "jump down", skip it.
            if climb <= 0:
                continue

            # Otherwise, allocate a ladder for this climb.
            heapq.heappush(bricks_allocation, -climb)
            bricks -= climb

            # If we've used all the bricks, and have no ladders remaining, then
            # we can't go any further.
            if bricks < 0 and ladders == 0:
                return i

            # Otherwise, if we've run out of bricks, we should replace the largest
            # brick allocation with a ladder.
            if bricks < 0:
                bricks += -heapq.heappop(bricks_allocation)
                ladders -= 1
        return len(heights) - 1


s = Solution_1()
heights = [4, 12, 2, 7, 3, 18, 20, 3, 19]
bricks = 10
ladders = 2
result = s.furthestBuilding(heights, bricks, ladders)
print(result)
