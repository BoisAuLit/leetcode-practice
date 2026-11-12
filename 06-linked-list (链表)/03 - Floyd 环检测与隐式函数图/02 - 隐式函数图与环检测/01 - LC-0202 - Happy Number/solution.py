class Solution:
    def isHappy(self, n: int) -> bool:
        def get_sum(n: int) -> int:
            res = 0
            while n:
                n, rem = divmod(n, 10)
                res += rem * rem
            return res

        slow, fast = n, get_sum(n)

        while slow != fast:
            fast = get_sum(fast)
            fast = get_sum(fast)
            slow = get_sum(slow)
        return fast == 1


s = Solution()
input_ = 101
result = s.isHappy(input_)
print(result)
