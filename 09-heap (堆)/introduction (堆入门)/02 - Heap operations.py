import heapq
import random

# ! Turn a list into heap ↔️
# This is done in-place
# ! Time complexity is: O(N)
heap = [2, 3, 5, 6, 8, 4, 12]
heapq.heapify(heap) # ⭐️
print(heap)

# ! Heap insertion 💉
# 1. Insert an element into the heap
# 2. Maintain the heap traits (min-heap, max-heap)
# ! 3. Time complexity O(logN)
heap = []
for _ in range(10):
    # Generate a random number in [1, 10]
    next_int = random.randint(1, 10)
    heapq.heappush(heap, next_int) # ⭐️
print(heap)

# ! Heap deletion ❌
# It only deletes the smallest element form the heap
# It still maintains the heap structure
# ! Time complexity: O(logN)
heap = [2, 3, 5, 6, 8, 4, 12]
length = len(heap)
for _ in range(length):
    heapq.heappop(heap)
    print(heap)

"""
If we create a heap by
1. heapify an already existing list, then
   the time complexity is O(N)

2. inserting n elements one by one, then
   the time comlexity is O(NlogN)

***********************************************

Every time we insert / delete using heapq.heappush, heapq.heappop,
the properties of the min-heap is preserved
1. Complete binary tree
2. Value of each node <= values of its descendants
"""
