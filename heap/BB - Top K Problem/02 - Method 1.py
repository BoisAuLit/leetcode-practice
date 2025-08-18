import heapq
from typing import List

def top_k_largest(nums: List[int], k: int) -> List[int]:
    """
    Approach 1 for Top-K Largest:
      1) Construct a Max-Heap (via negatives).
      2) Add all elements.
      3) Pop K times into result T.
    Returns the K largest in descending order.
    """
    if k <= 0 or not nums:
        return []
    k = min(k, len(nums))

    # Max-heap via negatives
    max_heap = [-x for x in nums]   # (Step 2) add all items
    heapq.heapify(max_heap)         # (Step 1) heap construction

    T = []
    for _ in range(k):              # (Steps 3–4) pop K times
        T.append(-heapq.heappop(max_heap))
    return T  # already largest-to-smallest


def top_k_smallest(nums: List[int], k: int) -> List[int]:
    """
    Approach 1 for Top-K Smallest:
      1) Construct a Min-Heap.
      2) Add all elements.
      3) Pop K times into result T.
    Returns the K smallest in ascending order.
    """
    if k <= 0 or not nums:
        return []
    k = min(k, len(nums))

    # Use a copy so we don't mutate caller's list
    min_heap = nums[:]              # (Step 2) add all items
    heapq.heapify(min_heap)         # (Step 1) heap construction

    T = []
    for _ in range(k):              # (Steps 3–4) pop K times
        T.append(heapq.heappop(min_heap))
    return T  # smallest-to-largest

nums = [7, 2, 9, 4, 1, 5]
print(top_k_largest(nums, 3))   # [9, 7, 5]
print(top_k_smallest(nums, 3))  # [1, 2, 4]
