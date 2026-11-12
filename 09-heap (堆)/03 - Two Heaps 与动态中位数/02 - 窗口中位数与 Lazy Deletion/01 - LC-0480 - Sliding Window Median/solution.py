"""LC-0480 - Sliding Window Median（第二轮自主新增）

Level 1 · 03 Two Heaps 与动态中位数 —— 双堆 + **Lazy Deletion（惰性删除）**
题目在问：大小为 k 的滑动窗口，每次输出窗口中位数。

为什么新增它（它补的是哪个缺口）：
  LC-0295 用双堆维护动态中位数，但那里**只会往里加元素，从不删除**。
  一旦窗口开始滑动，就要**从堆中间删掉一个任意元素** ——
  而**堆不支持 O(log n) 删除任意元素**（只能删堆顶）。
  这就逼出了 **Lazy Deletion** 这个通用技巧，它在 LC-3408（本专题已有）、
  各种「带过期的优先队列」里反复出现。本专题原本没有专门练这一点的题。

决定性观察：
  1. **双堆结构**（和 LC-0295 完全一样）：
     - `small`：最大堆（存负数），放较小的一半
     - `large`：最小堆，放较大的一半
     - 不变量：`len(small) == len(large)` 或 `len(small) == len(large) + 1`
     - 中位数：k 奇数 → `small` 堆顶；k 偶数 → 两个堆顶的平均。
  2. **Lazy Deletion**：要删除的元素如果不在堆顶，就**不真的删**，
     只在一个 `to_delete` 计数表里记一笔「这个值欠删一次」。
     等它**浮到堆顶时再真正弹出**。
  3. 但这样堆的 `len()` 就不等于「有效元素数」了 ⟹
     必须另外维护 **`small_size` / `large_size`** 两个计数器来做平衡判断，
     **不能用 `len(heap)`**。这是本题最容易错的地方。
  4. 每次操作后调用 `prune()` 清理两个堆顶的失效元素，保证「堆顶一定有效」。

```
balance 规则（用逻辑size，不用 len）：
  small_size > large_size + 1 → 把 small 顶搬到 large
  small_size < large_size     → 把 large 顶搬到 small
每次搬完都要 prune
```

复杂度：**O(n log n)** —— 每个元素入堆一次、最终出堆一次（惰性也只会出一次）。
      空间 O(n)（最坏情况下失效元素积压）。
      **不是 O(n log k)**，因为失效元素可能在堆里滞留。

另一种解法：`SortedList`（第三方 `sortedcontainers`）可以 O(log k) 插入/删除 +
      O(1) 取中位数，总共 O(n log k)，代码短得多。但标准库没有，
      面试里要么手写双堆、要么说明依赖。本文件的 Solution_2 用排序列表 + 二分
      模拟了这个思路（插入是 O(k) 的 list.insert，总体 O(nk)），作为对拍基准。

边界：
  - k == 1（中位数就是元素本身）
  - k == n（只有一个窗口）
  - 全部相同的元素
  - 含极大值（题目有 2^31-1 的测试点，Python 无溢出问题）
  - 偶数 k 的平均值必须是浮点
"""

import heapq
from collections import defaultdict
from typing import List


##################################################################################################
##### ! Solution 1: 双堆 + Lazy Deletion + 独立维护逻辑 size
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：所有「优先队列里要删除非堆顶元素」的场景；和 LC-0295 共用双堆骨架
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        small: List[int] = []            # ! 最大堆（存负数），较小的一半
        large: List[int] = []            # ! 最小堆，较大的一半
        # ! 删除标记必须**分边记**：如果两个堆里都有同一个值（重复元素跨越中位线），
        # ! 共用一张表会让 prune 时「这一笔删除」被错误的那一边消费掉，
        # ! 于是计数器和堆内容就对不上了。这是本题最隐蔽的坑。
        del_small: defaultdict = defaultdict(int)
        del_large: defaultdict = defaultdict(int)
        small_size = large_size = 0      # ! 逻辑大小，**不能用 len(heap)**（堆里有失效元素）

        def prune_small():
            while small and del_small[-small[0]] > 0:
                del_small[-small[0]] -= 1
                heapq.heappop(small)

        def prune_large():
            while large and del_large[large[0]] > 0:
                del_large[large[0]] -= 1
                heapq.heappop(large)

        def move_small_to_large():
            nonlocal small_size, large_size
            prune_small()
            heapq.heappush(large, -heapq.heappop(small))
            small_size -= 1
            large_size += 1

        def move_large_to_small():
            nonlocal small_size, large_size
            prune_large()
            heapq.heappush(small, -heapq.heappop(large))
            large_size -= 1
            small_size += 1

        def rebalance():
            """维持 small_size == large_size 或 small_size == large_size + 1。"""
            while small_size > large_size + 1:
                move_small_to_large()
            while small_size < large_size:
                move_large_to_small()
            prune_small()
            prune_large()

        def add(num):
            nonlocal small_size, large_size
            prune_small()
            if small_size == 0 or num <= -small[0]:
                heapq.heappush(small, -num)
                small_size += 1
            else:
                heapq.heappush(large, num)
                large_size += 1
            rebalance()

        def remove(num):
            nonlocal small_size, large_size
            prune_small()
            # ! 必须在打标记**之前**判断它属于哪一半（prune 可能把它从堆顶弹走）
            if small_size > 0 and num <= -small[0]:
                del_small[num] += 1       # ! 标记只记在它所属的那一边
                small_size -= 1
            else:
                del_large[num] += 1
                large_size -= 1
            rebalance()

        def median():
            prune_small()
            prune_large()
            if k % 2:
                return float(-small[0])
            return (-small[0] + large[0]) / 2.0

        res = []
        for i, x in enumerate(nums):
            add(x)
            if i >= k:
                remove(nums[i - k])
            if i >= k - 1:
                res.append(median())
        return res


##################################################################################################
##### ! Solution 2: 维护一个有序列表 + 二分插入/删除（基准答案，用来对拍）
##### ! 时间复杂度: O(n·k)（list.insert 是 O(k)）   空间复杂度: O(k)
##### ! 适用：正确性参照；也是 SortedList 解法的朴素版（有 sortedcontainers 时是 O(n log k)）
##################################################################################################


class Solution_2:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        import bisect
        window = sorted(nums[:k])
        res = []
        for i in range(k, len(nums) + 1):
            if k % 2:
                res.append(float(window[k // 2]))
            else:
                res.append((window[k // 2 - 1] + window[k // 2]) / 2.0)
            if i == len(nums):
                break
            window.pop(bisect.bisect_left(window, nums[i - k]))   # ! 真删
            bisect.insort(window, nums[i])
        return res


if __name__ == "__main__":
    import random

    cases = [([1, 3, -1, -3, 5, 3, 6, 7], 3), ([1, 2, 3, 4, 2, 3, 1, 4, 2], 3),
             ([1], 1), ([1, 2], 2), ([5, 5, 5, 5], 2), ([2147483647, 2147483647], 2)]
    for nums, k in cases:
        a = Solution_1().medianSlidingWindow(nums, k)
        b = Solution_2().medianSlidingWindow(nums, k)
        assert all(abs(x - y) < 1e-9 for x, y in zip(a, b)) and len(a) == len(b), (nums, k, a, b)
        print(f"{nums}, k={k} -> {a}")

    for _ in range(1000):                # ! 随机对拍，含大量重复值（惰性删除最容易在这里出错）
        n = random.randint(1, 12)
        nums = [random.randint(0, 5) for _ in range(n)]
        k = random.randint(1, n)
        a = Solution_1().medianSlidingWindow(nums, k)
        b = Solution_2().medianSlidingWindow(nums, k)
        assert len(a) == len(b) and all(abs(x - y) < 1e-9 for x, y in zip(a, b)), (nums, k, a, b)
    print("随机对拍 1000 组通过 ✓（双堆+惰性删除 == 有序列表真删）")
