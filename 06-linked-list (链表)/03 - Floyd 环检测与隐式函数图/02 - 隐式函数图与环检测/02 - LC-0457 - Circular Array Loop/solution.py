"""LC-0457 - Circular Array Loop
https://leetcode.com/problems/circular-array-loop/submissions/2191100274/

Floyd 判圈 · 把"数组下标"当成链表的 next 指针
题目在问：nums[i] 表示从 i 往前(正)或往后(负)走 nums[i] 步(环形数组)，问存不存在一个**合法环**
合法环的三个条件：长度 > 1、环里所有数**同号**、走到底能回到起点
next 指针是什么：j = (i + nums[i]) % n   —— 这就是本题唯一的"链表化"动作

三个坑（都是 WA 的来源）：
  1. 长度 1 不算：j == i 时直接判死，不能当成环
  2. 必须同号：走一步就要检查 (nums[j] > 0) == forward，中途变号就断掉
  3. 负数取模：Python 的 % 自动给非负结果，C++/Java 要写 ((i + nums[i]) % n + n) % n
保证 nums[i] != 0（题目约束），所以 0 可以安全当"已访问"的标记用
"""

##################################################################################################
##### ! Solution 1: Floyd 快慢指针 + 清零标记
##### ! 时间复杂度: O(n)   空间复杂度: O(1)   每个格子只会被清零一次，所以总步数是摊还 O(n)
##### ! 适用: 允许改输入数组时的最优解；O(1) 空间是本题的面试考点
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################

class Solution_1:
    def circularArrayLoop(self, nums: list[int]) -> bool:
        n = len(nums)

        def get_next(i, forward):
            if nums[i] == 0 or (nums[i] > 0) != forward:
                return -1

            j = (i + nums[i]) % n

            if j == i or nums[j] == 0 or (nums[j] > 0) != forward:
                return -1

            return j

        for i in range(n):
            if nums[i] == 0:
                continue

            forward = nums[i] > 0
            slow = fast = i

            # Floyd's Cycle Detection
            while True:
                slow = get_next(slow, forward)
                fast = get_next(fast, forward)

                if fast != -1:
                    fast = get_next(fast, forward)

                if slow == -1 or fast == -1:
                    break

                if slow == fast:
                    return True

            # Mark visited nodes as 0
            cur = i
            while nums[cur] != 0 and (nums[cur] > 0) == forward:
                nxt = (cur + nums[cur]) % n
                nums[cur] = 0
                cur = nxt

        return False


##################################################################################################
##### ! Solution 2: 暴力 —— 每个起点走 n + 1 步
##### ! 时间复杂度: O(n²)   空间复杂度: O(1)   n 个起点，每个最多走 n + 1 步
##### ! 适用: 想不起 Floyd 时的保底写法；不改输入数组
##### ! 原理: n + 1 步里访问了 n + 1 个格子，鸽巢原理保证必有重复 = 有环
##################################################################################################


class Solution_2:
    def circularArrayLoop(self, nums: list[int]) -> bool:
        n = len(nums)

        for start in range(n):
            forward = nums[start] > 0
            cur = start

            for _ in range(n + 1):
                nxt = (cur + nums[cur]) % n
                # ! 坑 1: nxt == cur 是长度 1 的自环，不算；坑 2: 变号就断
                if nxt == cur or (nums[nxt] > 0) != forward:
                    break
                cur = nxt
            else:
                # ! for ... else: n + 1 步一次没断过 → 必有重复格子 → 有合法环
                return True

        return False


##################################################################################################
##### ! Solution 3: 染色法 —— 记"这一轮走过"还是"上一轮走过"
##### ! 时间复杂度: O(n)   空间复杂度: O(n)   owner 数组，每个格子只被某一轮染一次
##### ! 适用: 不允许改输入数组时的 O(n) 解；也是函数图找环的通用套路
##### ! 为什么记忆化是对的: 每个格子的 next 完全由 nums[i] 自己决定(方向也是)，
##### !   所以"从 X 出发有没有环"是格子的固有属性，上一轮算过的结论这一轮直接能用
##################################################################################################


class Solution_3:
    def circularArrayLoop(self, nums: list[int]) -> bool:
        n = len(nums)
        owner = [0] * n  # ! 0 = 没走过；否则 = 第几轮(start + 1)走到的，用轮次区分"自己的脚印"

        for start in range(n):
            if owner[start]:
                continue

            forward = nums[start] > 0
            cur = start

            while owner[cur] == 0 and (nums[cur] > 0) == forward:
                owner[cur] = start + 1
                nxt = (cur + nums[cur]) % n
                if nxt == cur:  # ! 坑 1: 长度 1 的自环，break 掉就不会进 else
                    break
                cur = nxt
            else:
                # ! 没 break 而是条件不成立退出：要么变号断了，要么踩到脚印
                if owner[cur] == start + 1:  # ! 踩到的是本轮自己的脚印 → 有环
                    return True

        return False


if __name__ == "__main__":
    cases = [
        ([2, -1, 1, 2, 2], True),       # 0 → 2 → 3 → 0，全正，长度 3
        ([-1, -2, -3, -4, -5, 6], False),
        ([1, -1, 5, 1, 4], True),
        ([-1, 2], False),               # 坑 2: 0 → 1 → 1，变号
        ([-2, 1, -1, -2, -2], False),   # 坑 1: 2 → 1 是正号，断
        ([3, 1, 2], True),
        ([1], False),                   # 坑 1: 唯一的环长度为 1
        ([2, 2, 2, 2], True),
    ]

    for i, sol in enumerate([Solution_1(), Solution_2(), Solution_3()], 1):
        got = [sol.circularArrayLoop(list(nums)) for nums, _ in cases]  # ! Solution_1 会改数组，必须传副本
        want = [expected for _, expected in cases]
        print(f"Solution_{i}: {'✅' if got == want else f'❌ got {got} want {want}'}")
