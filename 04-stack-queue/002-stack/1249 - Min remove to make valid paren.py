from collections import defaultdict

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        mapping = defaultdict(list)
        indexes_to_remove = set()
        for index, char in enumerate(s):
            if char == "(":
                mapping["("].append(index)
            if char == ")":
                if mapping["("]:
                    mapping["("].pop()
                else:
                    indexes_to_remove.add(index)
        indexes_to_remove.update(mapping["("])
        return "".join(char for index, char in enumerate(s) if index not in indexes_to_remove)


s = Solution()
input_ = "lee(t(c)o)de)"
input_ = "a)b(c)d"
input_ = "))(("
result = s.minRemoveToMakeValid(input_)
print(result)
