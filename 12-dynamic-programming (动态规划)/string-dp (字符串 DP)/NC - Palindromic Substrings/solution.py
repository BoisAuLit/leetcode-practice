class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)

        # 从 (l, r) 向两边扩散，返回以这个中心能构成的回文个数
        def expand(l: int, r: int) -> int:
            count = 0
            while l >= 0 and r < n and s[l] == s[r]:
                l -= 1
                r += 1
                count += 1
            return count

        # 奇数中心 (i, i) + 偶数中心 (i, i+1)
        return sum(expand(i, i) + expand(i, i + 1) for i in range(n))


s = Solution()
input_ = "aaa"
result = s.countSubstrings(input_)
print(result)
