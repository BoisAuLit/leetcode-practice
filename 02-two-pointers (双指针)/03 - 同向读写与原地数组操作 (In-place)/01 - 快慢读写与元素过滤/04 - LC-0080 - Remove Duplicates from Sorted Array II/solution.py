"""LC-0080 - Remove Duplicates from Sorted Array II

Level 1 · 03 同向读写与原地数组操作 —— Read/Write Pointers 的推广（每个值最多留 k 个）
题目在问：有序数组原地去重，但每个值**最多保留两个**，返回新长度

决定性观察：LC-0026 的判断是「和上一个保留的不同就写」，这题只要把「上一个」
      换成「**往前数第 k 个保留的**」：如果 `nums[read] != nums[write - k]`，
      说明再写一个也不会让同一个值出现 k+1 次。k = 1 就退化成 LC-0026。

循环不变量：
  - `nums[0:write]` 永远是一个合法答案（有序、每个值出现次数 <= k）
  - `write <= read`，所以写入永远不会覆盖还没读到的数据
  这两条合起来就是「同向读写」这一类的全部安全性保证。

为什么只比较 `nums[write - k]` 就够：因为数组有序，`nums[0:write]` 里相同的值一定相邻。
  若 `nums[read] == nums[write - k]`，那 `nums[write-k:write]` 这 k 个全等于它，已经满额。

坑：
  - `write < k` 时要直接写（前 k 个无条件保留），否则 `write - k` 会变成负下标，
    Python 的负下标不报错但会从尾部取值，静默出错
  - 比较的是 `nums[write - k]` 而不是 `nums[read - k]`：read 那边还有没被保留的重复值
  - 返回的是长度 `write`，不是数组本身；write 之后的内容题目不关心
"""

from typing import List

K = 2  # ! 每个值最多保留几个；改成 1 就是 LC-0026


##################################################################################################
##### ! Solution 1: 读写双指针，和「往前第 k 个保留值」比较
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：26 / 80 / 「最多保留 k 个」的通解，一行改 k 即可；本层最值得记的一个模板
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def removeDuplicates(self, nums: List[int]) -> int:
        write = 0
        for read in range(len(nums)):
            # ! write < K：前 K 个无条件保留（也避免 write - K 变成负下标）
            if write < K or nums[read] != nums[write - K]:
                nums[write] = nums[read]
                write += 1
        return write


##################################################################################################
##### ! Solution 2: 显式记录当前值出现了几次
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：思路最直白，不依赖「数组有序 ⇒ 相同值相邻」这个性质，所以**无序数组也能用**
##################################################################################################


class Solution_2:
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0
        write, run = 1, 1  # run = 当前值已经保留了几个
        for read in range(1, len(nums)):
            run = run + 1 if nums[read] == nums[read - 1] else 1
            if run <= K:
                nums[write] = nums[read]
                write += 1
        return write


if __name__ == "__main__":
    import random
    from collections import Counter
    cases = [([1, 1, 1, 2, 2, 3], [1, 1, 2, 2, 3]),
             ([0, 0, 1, 1, 1, 1, 2, 3, 3], [0, 0, 1, 1, 2, 3, 3]),
             ([1], [1]), ([], []), ([1, 1], [1, 1]), ([1, 1, 1], [1, 1])]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for nums, want in cases:
            a = nums[:]
            k = sol.removeDuplicates(a)
            assert a[:k] == want, f"{type(sol).__name__} {nums}: got {a[:k]}, want {want}"
    rng = random.Random(80)
    for _ in range(2000):
        nums = sorted(rng.randint(0, 5) for _ in range(rng.randint(0, 12)))
        want = [v for v, c in sorted(Counter(nums).items()) for _ in range(min(c, K))]
        for sol in sols:
            a = nums[:]
            k = sol.removeDuplicates(a)
            assert a[:k] == want, (type(sol).__name__, nums, a[:k], want)
    print("2 个解法全过（含 2000 组随机对拍）")
