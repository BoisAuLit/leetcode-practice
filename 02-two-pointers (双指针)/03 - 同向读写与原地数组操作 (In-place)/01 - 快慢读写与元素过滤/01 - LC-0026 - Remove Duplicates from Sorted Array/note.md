# Remove Duplicates from Sorted Array 笔记

### 📝 2026-10-03 - retry 1

```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        # ! 只需要一个初始变量 insertIndex 即可
        insertIndex = 1
        for i in range(1, len(nums)):
            # ! 当且仅当当前值与上一个值不一样的时候, 才将 insertIndex 往前推进
            if nums[i - 1] != nums[i]:
                nums[insertIndex] = nums[i]
                insertIndex = insertIndex + 1
        # ! 最后返回 insertIndex 即可
        return insertIndex
```
