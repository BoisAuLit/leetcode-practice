import heapq
from typing import List


def top_k_smallest_fast(nums: List[int], k: int) -> List[int]:
    """
    时间复杂度: O(n log k)
    空间复杂度: O(k)
    维护“大小为 k 的最大堆（用负号模拟）”，直接 heappushpop(heap, -x)。
    """
    if k <= 0:
        return []
    if k >= len(nums):
        return sorted(nums)

    heap = []  # 存 -x
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, -x)
        else:
            # 关键点：
            # 若 x < -heap[0]（更小），则 -x > heap[0] 吗？注意这里用 heappushpop 的“镜像逻辑”：
            # heappushpop 会：先 push(-x)，再 pop 最小的负数。
            # - 当 x < -heap[0]：-x > heap[0] 不一定，但行为正确：最终会把“最小的负数”（也就是当前集合里最大的值）弹走，保留更小的 x。
            # - 当 x >= -heap[0]：-x <= heap[0]，push 后立刻把 -x 自己弹掉 → 堆不变，相当于“跳过”。
            heapq.heappushpop(heap, -x)

    return sorted(-v for v in heap)
