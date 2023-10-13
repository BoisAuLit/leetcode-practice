class Solution:
    
    def biggerThan(self, int1: str, int2: str) -> bool:
        if len(int1) < len(int2):
            return False
        for a, b in zip(int1, int2):
            if a > b:
                return True
            if a < b:
                return False
        return False
    
    def reverse(self, x: int) -> int:
        max_ = str(2**31-1)
        min_ = str(-2**31)[1:]
        strX = str(x)
        if x >= 0:
            reversedX = strX[::-1]
            return 0 if self.biggerThan(reversedX, max_) else int(reversedX)
        reversedX = strX[1:][::-1]
        return 0 if self.biggerThan(reversedX, min_) else -int(reversedX)

s = Solution()

# Expecting 321 --> Positive number within range
input_ = 123

# Expecting 0 --> Positive number out of range
input_ = 1000000009

# Expecting 0
# input_ = 0

# Expecting -321 --> Negative number within range
input_ = -123

# Expecting 0 --> Negative number out of range
input_ = -1000000009

# Expecting -2143847412
input_ = -2147483412

result = s.reverse(input_)

print(result)

"""

"""
