# Kth Missing Positive Number 笔记

### 📝 2026-09-27 - retry 1

```python
class Solution:
    # ============================================================
    # 三条精髓,记住就能重写:
    # ① 不缺数时 arr[i] == i+1,所以 arr[i] 之前缺失数量 = arr[i] - i - 1,随 i 单调不减
    # ② 第 k 个缺失数 x:1..x 共 x 个数 = k 个缺失 + i 个存在(arr[0..i-1]) → x = k + i
    #    其中 i = 第一个满足 arr[i]-i-1 >= k 的下标;找不到时 i = n,公式不变
    # ③ "第一个满足条件的下标" = 找左边界二分 = bisect_left
    # ============================================================
    def findKthPositive(self, arr: List[int], k: int) -> int:
        l, r = 0, len(arr)  # hi = n 表示"答案在末尾之后"
        while l < r:
            mid = (l + r) // 2
            if arr[mid] - mid - 1 >= k:  # 缺得够了 → 答案在 mid 或更左
                r = mid
            else:  # 缺得不够 → 答案在 mid 右边
                l = mid + 1
        return k + l

    # 一行版(Python ≥ 3.10):在下标序列上二分,key 里同时拿到 i 和 arr[i]
    def findKthPositive_bisect(self, arr: List[int], k: int) -> int:
        return k + bisect_left(range(len(arr)), k, key=lambda i: arr[i] - i - 1)
```
