class Solution:
    def removeDuplicateLetters(self, s: str) -> int:
        last_occurrence = {letter: index for index, letter in enumerate(s)}
        result = []
        seen = set()
        for index, letter in enumerate(s):
            if letter not in seen:
                while (
                    result
                    and index < last_occurrence[result[-1]]
                    and letter < result[-1]
                ):
                    seen.remove(result.pop())
                result.append(letter)
                seen.add(letter)
        return "".join(result)


s = Solution()


input_ = "bcabc"  # Expecting "abc"
# input_ = "cbacdcbc" # "acdb"
# input_ = "kbakdkbk"  # "adbk"
result = s.removeDuplicateLetters(input_)
print(result)

"""

"""
