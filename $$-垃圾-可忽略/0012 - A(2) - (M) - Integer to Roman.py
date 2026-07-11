class Solution:
    def intToRoman(self, num: int) -> str:
        mapping = {1: "IVX", 10: "XLC", 100: "CDM", 1000: "M"}
        result = []
        base = 1
        while num:
            """
            ! In each iteration, we only take care of one digit place,
            ! such as ones place, tens place, hundreds place, etc.

            We only care about the 3 letters at each place.
            """

            # ! Step 1: Obtain the digit
            digit = num % 10

            # ! If the digit is 0, we can just continue to the next place
            if digit == 0:
                base *= 10
                num //= 10
                continue

            # ! Step 2: Obtain the 3 digits in the place from the hashmap
            letters = mapping[base]

            # ! Step 3: Each if condition below is a different case
            if 1 <= digit <= 3:
                result.append(letters[0] * digit)
            elif digit == 4:
                result.append(letters[0] + letters[1])
            elif digit == 5:
                result.append(letters[1])
            elif 6 <= digit <= 8:
                result.append(letters[1] + letters[0] * (digit - 5))
            else:
                result.append(letters[0] + letters[2])

            """
            In the end, we need to:
            1. update the base
            2. integer divide the number by 10
            """
            base *= 10
            num //= 10
        return "".join(reversed(result))


s = Solution()
input_ = 1349
result = s.intToRoman(input_)
print(result)
