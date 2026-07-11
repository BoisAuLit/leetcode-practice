import heapq
from typing import List


def top_k_smallest(nums: List[int], k: int) -> List[int]:
    """
    时间复杂度: O(n log k)
    空间复杂度: O(k)
    维护一个“最大堆”（用负号模拟）的大小为 k 的集合，始终保存目前为止最小的 k 个元素。
    """
    if k <= 0:
        return []
    if k >= len(nums):
        return sorted(nums)  # 如需从小到大输出

    heap = []  # 存放负数，min-heap of negatives == max-heap by value

    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, -x)
        elif x < -heap[0]:
            heapq.heappop(heap)  # 弹出当前集合里的“最大值”
            heapq.heappush(heap, -x)  # 加入更小的 x

    # 取负还原，并从小到大返回
    return sorted(-v for v in heap)


# --- demo ---
if __name__ == "__main__":
    data = [5, 1, 9, 3, 12, 7, 2, 10, 6, 8, 15, 11, 4, 14, 13]
    print(top_k_smallest(data, 5))  # 例如: [1, 2, 3, 4, 5]
