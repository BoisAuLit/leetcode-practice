"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def validWordAbbreviation(self, word: str, abbr: str) -> bool:
        length = len(word)
        acc_length = 0
        digits = []
        for index, char in enumerate(abbr):
            if char.isdigit():
                if char == "0":
                    if index == 0:
                        return False
                    if abbr[index - 1].isalpha():
                        return False
                digits.append(char)
                if index == len(abbr) - 1:
                    acc_length += int("".join(digits))
            else:
                if len(digits) > 0:
                    acc_length += int("".join(digits))
                if acc_length >= length or word[acc_length] != char:
                    return False
                digits = []
                acc_length += 1
                if acc_length > length:
                    return False
        return acc_length == length


s = Solution()

# # Expecting True
# word = "internationalization"
# abbr = "i12iz4n"

# # Expecting False
# word = "apple"
# abbr = "a2e"

# # Expecting True
# word = "internationalization"
# abbr = "i5a11o1"

# # Expecting False
# word = "word"
# abbr = "3e"

# # Expecting False
# word = "hi"
# abbr = "2i"

# Expecting True
word = "abbreviation"
abbr = "a10n"

result = s.validWordAbbreviation(word, abbr)
print(result)
