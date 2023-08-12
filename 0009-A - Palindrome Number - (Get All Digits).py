"""
Time complexity: O(n)
Space complexity: O(n)
"""


class Solution:
    def isPalindrome(self, x: int) -> bool:
        # 💥💥💥💥💥💥💥💥💥
        # Don't forget to deal with negative numbers
        if x < 0:
            return False
        # 💥💥💥💥💥💥💥💥💥
        array = []
        while True:
            x, r = divmod(x, 10)
            array.append(r)
            if x == 0:
                break
        for i in range(len(array) // 2):
            if array[i] != array[-(i + 1)]:
                return False
        return True


s = Solution()
input_ = -123
result = s.isPalindrome(input_)
print(result)
