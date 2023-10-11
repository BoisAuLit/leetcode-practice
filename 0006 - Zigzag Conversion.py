from itertools import zip_longest


class Solution:
    def convert(self, s: str, numRows: int) -> str:
        n = 2 * numRows - 2
        if n == 0:
            return s
        firstRow = s[::n]
        lastRow = s[numRows - 1 :: n]
        middle = []
        for i in range(1, numRows - 1):
            for a, b in zip_longest(s[i::n], s[n - i :: n], fillvalue=""):
                middle.extend([a, b])

        return firstRow + "".join(middle) + lastRow


s = Solution()
input_ = "PAYPALISHIRING"
result = s.convert(input_, 3)
print(result)
