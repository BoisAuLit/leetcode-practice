class Solution:
    def titleToNumber(self, columnTitle: str) -> int:
        power = 1
        column = 0
        for i in range(len(columnTitle) - 1, -1, -1):
            column += (ord(columnTitle[i]) - ord("A") + 1) * power
            power *= 26
        return column


s = Solution()
input_ = "ZZ"
result = s.titleToNumber(input_)
print(result)
