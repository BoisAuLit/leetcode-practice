class Solution:
    def minSwaps(self, s: str) -> int:
        length = len(s)

        nb_ones = len([1 for c in s if c == "1"])
        nb_zeroes = length - nb_ones
        if abs(nb_zeroes - nb_ones) >= 2:
            return -1

        if nb_ones == nb_zeroes:
            nb_ones_even = len([1 for c in s[::2] if c == "1"])
            return min(nb_ones_even, length // 2 - nb_ones_even)

        dominant = "1" if nb_ones > nb_zeroes else "0"
        nb_dominant_even = len([1 for c in s[::2] if c == dominant])
        return (length + 1) // 2 - nb_dominant_even


s = Solution()

# Test case 1: Expecting 1
# input_ = "111000"

# Test case 2: Expecting 0
# input_ = "010"

# Test case 3: Expecting -1
input_ = "1110"


result = s.minSwaps(input_)
print(result)
