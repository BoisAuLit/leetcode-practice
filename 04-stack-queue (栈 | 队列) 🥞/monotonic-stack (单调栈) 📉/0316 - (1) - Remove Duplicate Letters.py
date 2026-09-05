"""

Given a string s, remove duplicate letters so that
every letter appears once and only once.

You must make sure your result is 
the [smallest in lexicographical order]
among all possible results.



Solution: Let the duplicate small letters (abcd..)
appear as early as possible.
"""


class Solution:
    """
    If the last added character can be removed to get a better result,
    then remove it.
    """
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
