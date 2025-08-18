import heapq
from typing import List


def top_k_smallest_heapreplace(nums: List[int], k: int) -> List[int]:
    """
    时间复杂度: O(n log k)
    空间复杂度: O(k)
    逻辑同上，但用 heapreplace 简化“pop 再 push”的两步操作。
    """
    if k <= 0:
        return []
    if k >= len(nums):
        return sorted(nums)

    heap = []  # 存 -x

    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, -x)
        elif x < -heap[0]:
            # heapreplace 等价于：先弹出堆顶，再压入新值
            heapq.heapreplace(heap, -x)
        # 否则 x 不够小，跳过

    return sorted(-v for v in heap)
