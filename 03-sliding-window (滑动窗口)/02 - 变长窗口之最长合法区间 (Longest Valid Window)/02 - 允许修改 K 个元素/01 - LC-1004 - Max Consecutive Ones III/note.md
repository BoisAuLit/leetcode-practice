# Max Consecutive Ones III 笔记

### 📝 2026-09-22 - retry 1

```python
class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        """
        找一段最长的连续区间,使得这段区间里0 的个数不超过 k。为什么等价?因为一段区间里如果 0 不超过 k 个,那我把这些 0 全翻成 1,这段就全是 1 了;反过来如果 0 超过 k 个,翻不完,这段就不可能全变成 1。所以"翻转"这个动作根本不用真的做,题目本质就是:找最长的、0 不超过 k 个的连续一段。
        """
        left = right = 0
        nb_zeros = 0 # ! 要数 0 的个数
        max_length = 0 # ! 要记录最大 length
        while right < len(nums):
            nb_zeros += int(nums[right] == 0)

            # ! 左边收缩, 直至合法为止
            while nb_zeros > k:
                nb_zeros -= int(nums[left] == 0)
                left += 1
            max_length = max(max_length, right - left + 1)
            right += 1 # ! 每次 right 只往前推进 1
        return max_length
```
