from typing import List


class Solution:
    def compress(self, chars: List[str]) -> int:
        count = 0
        prev = chars[0]
        i = 0
        for char in chars + ["48"]:
            if char == prev:
                count += 1
                continue

            chars[i] = prev
            i += 1
            prev = char
            if count == 1:
                continue

            if count < 10:
                chars[i] = str(count)
                i += 1
                count = 1
                continue

            digit_count = 0
            j = i

            while count != 0:
                count, rem = divmod(count, 10)
                digit_count += 1
                chars[j] = str(rem)
                j += 1
            j -= 1
            l, r = i, j
            while l < r:
                chars[l], chars[r] = chars[r], chars[l]
                l += 1
                r -= 1
            i = j + 1
            count = 1

        return i


s = Solution()
chars = ["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]
# chars = ["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]
# chars = [
#     "a",
#     "a",
#     "b",
#     "b",
#     "c",
#     "c",
#     "c",
#     "c",
#     "c",
#     "c",
#     "c",
#     "c",
#     "c",
#     "c",
#     "c",
#     "c",
#     "c",
#     "c",
#     "c",
# ]
print(f"Before = {chars}")
result = s.compress(chars)
print(result)
print(f"After =  {chars}")
