"""LC-2401 - Longest Nice Subarray

Level 1 · 02 最长合法区间 —— 窗口状态可以不是频率表，而是一个 **bitmask（位掩码）**
题目在问：最长的子数组，使其中**任意两个数按位与都等于 0**

决定性观察：
  1. 「任意两个数两两 AND 为 0」⟺ **这些数用到的二进制位互不重叠**。
     所以窗口状态只要一个整数 `used`（窗口内所有数的 OR），
     判断新元素能不能进就是一句 `used & x == 0`。
  2. 这正是 LC-0003「窗口内字符不重复」的同构版本 —— 把「字符」换成「二进制位」，
     把「哈希集合」换成「位掩码」。**同一个模板，状态换了个表示法。**

Loop Invariant：`used` 恰好等于窗口 `[left, right]` 内所有元素的按位或，
      且这些元素的二进制位两两不重叠（即窗口合法）。

Window Shrinking Rule：`used & x != 0`（有位冲突）时从左边吐元素，
      吐出时 `used ^= nums[left]`（因为位不重叠，XOR 就是精确的「移除」）。

正确性简证：位不重叠 ⇒ OR 等于 XOR 等于相加，所以移除一个元素可以用 XOR 精确撤销，
      不需要像频率表那样计数。这也是为什么这题能用一个整数当状态。

另外：答案上界是 30 左右（数值 < 2^30，最多 30 个互不重叠的非零位），
      不过写成滑动窗口更自然，也不需要用到这个结论。

坑：
  - 吐元素时用 `^=` 而不是 `-=`，虽然这里两者等价，但 `^=` 表达的是「撤销这些位」
  - 0 这个元素和谁都不冲突，窗口可以无限长地包含多个 0 —— 代码天然支持，别特判
  - 内层必须是 while（可能要连吐好几个才腾出冲突的位）
"""

from typing import List


##################################################################################################
##### ! Solution 1: 变长窗口 + bitmask 状态
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：窗口约束是「元素之间互不冲突」时的通解；和 LC-0003 是同一个骨架
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def longestNiceSubarray(self, nums: List[int]) -> int:
        used = 0           # ! 窗口内所有数的按位或 = 已被占用的位
        left = 0
        best = 0
        for right, x in enumerate(nums):
            while used & x:                 # ! 有位冲突就从左边吐
                used ^= nums[left]          # ! 位不重叠，XOR 精确撤销
                left += 1
            used |= x
            best = max(best, right - left + 1)
        return best


##################################################################################################
##### ! Solution 2: 对每一位单独计数（把 bitmask 退化成 30 个计数器）
##### ! 时间复杂度: O(30n)   空间复杂度: O(30)
##### ! 适用：说明「bitmask 其实就是 30 个 0/1 频率表压成一个整数」；想不到位运算时的退路
##################################################################################################


class Solution_2:
    def longestNiceSubarray(self, nums: List[int]) -> int:
        BITS = 32
        cnt = [0] * BITS
        left = 0
        best = 0
        for right, x in enumerate(nums):
            for b in range(BITS):
                if x >> b & 1:
                    cnt[b] += 1
            while any(c > 1 for c in cnt):   # ! 某一位被占了两次 ⇒ 不合法
                out = nums[left]
                for b in range(BITS):
                    if out >> b & 1:
                        cnt[b] -= 1
                left += 1
            best = max(best, right - left + 1)
        return best


if __name__ == "__main__":
    import random
    cases = [([1, 3, 8, 48, 10], 3), ([3, 1, 5, 11, 13], 1), ([0, 0, 0], 3),
             ([1], 1), ([1, 2, 4, 8], 4)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for nums, want in cases:
            got = sol.longestNiceSubarray(nums[:])
            assert got == want, f"{type(sol).__name__} {nums}: got {got}, want {want}"
    rng = random.Random(2401)
    for _ in range(2000):
        nums = [rng.randint(0, 15) for _ in range(rng.randint(1, 9))]
        def ok(seg):
            return all(a & b == 0 for i, a in enumerate(seg) for b in seg[i + 1:])
        want = max(j - i + 1 for i in range(len(nums)) for j in range(i, len(nums))
                   if ok(nums[i:j + 1]))
        for sol in sols:
            assert sol.longestNiceSubarray(nums[:]) == want, (type(sol).__name__, nums, want)
    print("2 个解法全过（含 2000 组随机对拍）")
