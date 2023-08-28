class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        p1 = p2 = 0
        while p1 < len(s):
            while p2 < len(t) and t[p2] != s[p1]:
                p2 += 1
            if p2 >= len(t):
                return False
            if p1 == len(s) - 1:
                return True
            p1 += 1
            p2 += 1
        return True


solution = Solution()

# Expecting True
# s = "abc"
# t = "ahbgdc"

# Expecting False
# s = "axc"
# t = "ahbgdc"

# Expecting False
s = ""
t = "ahbgdc"



result = solution.isSubsequence(s, t)
print(result)

"""

"""
