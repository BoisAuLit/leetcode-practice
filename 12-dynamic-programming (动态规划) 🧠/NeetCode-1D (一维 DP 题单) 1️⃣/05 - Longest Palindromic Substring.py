class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)

        # 从 (l, r) 向两边扩散，返回这个中心能构成的最长回文子串
        def expand(l: int, r: int) -> str:
            while l >= 0 and r < n and s[l] == s[r]:
                l -= 1
                r += 1
            return s[l + 1 : r]

        res = ""
        for i in range(n):
            # 奇数中心 (i, i) + 偶数中心 (i, i+1)
            for curr in (expand(i, i), expand(i, i + 1)):
                if len(curr) > len(res):
                    res = curr
        return res


s = Solution()
input_ = "ababd"
result = s.longestPalindrome(input_)
print(result)
