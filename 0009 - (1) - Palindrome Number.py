"""
Time complexity: O(log10n)
Space complexity: O(1)
"""


# Solution 1 --> Reversing entire number 👍
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False

        reversed_num = 0
        temp = x

        while temp != 0:
            digit = temp % 10
            reversed_num = reversed_num * 10 + digit
            temp //= 10

        return reversed_num == x


# Solution 2 --> Half Palindrome
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0 or (x != 0 and x % 10 == 0):
            return False

        reversed_num = 0

        while x > reversed_num:
            reversed_num = reversed_num * 10 + x % 10
            x //= 10

        return x == reversed_num or x == reversed_num // 10

# Solution 3 --> Get all digits ❌
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        array = []
        while x != 0:
            array.append(x % 10)
            x //= 10
        for i in range(len(array) // 2):
            if array[i] != array[-(i + 1)]:
                return False
        return True



s = Solution()
input_ = 10
result = s.isPalindrome(input_)
print(result)
