class Solution_Using_Python_Built_Function:
    def mapHex(self, s: str) -> str:
        if s == "1":
            return "I"
        elif s == "0":
            return "O"
        else:
            return s

    def toHexspeak(self, num: str) -> str:
        mappedString = [self.mapHex(x) for x in hex(int(num))[2:].upper()]
        if any(char in "23456789" for char in mappedString):
            return "ERROR"
        return "".join(mappedString)

# 👍👍👍👍👍👍👍👍👍👍👍
class Solution_Bit_Manipulation:
    def toHexspeak(self, num: str) -> str:
        num = int(num)
        mask = 0b1111
        ans = []
        while num != 0:
            digit = num & mask
            if 1 < digit < 10:
                return "ERROR"
            num >>= 4
            ans.append(digit)

        hexdig = "OI23456789ABCDEF"
        return "".join(hexdig[d] for d in reversed(ans))


s = Solution_Bit_Manipulation()
# input_ = "257" # Expecting "IOI"
input_ = "747823223228"  # Expecting "AEIDBCDIBC"
# input_ = "3" # Expecting "ERROR"
result = s.toHexspeak(input_)
print(result)

"""

"""
