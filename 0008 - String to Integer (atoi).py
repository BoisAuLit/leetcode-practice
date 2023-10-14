class Solution:
    def myAtoi(self, input: str) -> int:
        sign = 1
        result = 0
        index = 0
        n = len(input)

        INT_MAX = pow(2, 31) - 1
        INT_MIN = -pow(2, 31)

        # Discard leading spaces
        while index < n and input[index] == " ":
            index += 1

        # Calculate sign
        if index < n and input[index] == "+":
            sign = 1
            index += 1
        elif index < n and input[index] == "-":
            sign = -1
            index += 1

        # Traverse next digits of input and stop if it is not a digit.
        # End of string is also non-digit character.
        while index < n and input[index].isdigit():
            digit = int(input[index])

            # Check overflow and underflow conditions.
            if (result > INT_MAX // 10) or (
                result == INT_MAX // 10 and digit > INT_MAX % 10
            ):
                # If integer overflowed return 2^31-1, otherwise if underflowed return -2^31.
                return INT_MAX if sign == 1 else INT_MIN
            result = 10 * result + digit
            index += 1
        
        return sign * result



s = Solution()
input_ = "123"
input_ = "   123"
input_ = "   +123"
input_ = "   -123"
input_ = "   -123###"
input_ = "   -#123"
input_ = "   -00000123"
input_ = "   -" + "2" * 40
input_ = "   +" + "2" * 40
input_ = "   " + "2" * 40
input_ = "   " + "2" * 40 + "#####"
result = s.myAtoi(input_)
print(result)
