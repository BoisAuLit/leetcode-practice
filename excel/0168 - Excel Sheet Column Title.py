class Solution:
    def convertToTitle(self, columnNumber: int) -> str:
        result = []
        while columnNumber:
            columnNumber, remainder = divmod(columnNumber - 1, 26)
            result.append(chr(65 + remainder))
        return "".join(reversed(result))


s = Solution()
input_ = 701  # Expecting "ZY"
result = s.convertToTitle(input_)
print(result)


# for i in range(1, 27):
#     print(s.convertNumber(i))

"""

"""
