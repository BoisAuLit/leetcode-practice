import heapq
from typing import List

def top_k_largest(nums: List[int], k: int) -> List[int]:
    """
    时间复杂度: O(n log k)
    空间复杂度: O(k)
    Maintain a min-heap of size k that stores the largest k elements.
    """
    if k <= 0:
        return []
    if k >= len(nums):
        return sorted(nums, reverse=True) # 如需从大到小输出

    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            """
            What heapreplace does:
            1. Remove the smallest element (top element of the min-heap)
            2. Add a new element
            """
            heapq.heapreplace(heap, x)
    return sorted(heap, reverse=True) # 如需从大到小输出

# --- demo ---
if __name__ == "__main__":
    data = [5, 1, 9, 3, 12, 7, 2, 10, 6, 8, 15, 11, 4, 14, 13]
    print(top_k_largest(data, 5))  # e.g. [15, 14, 13, 12, 11]
