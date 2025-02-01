from typing import List


class Solution:
    def reorderLogFiles(self, logs: List[str]) -> List[str]:
        letter_logs = [log for log in logs if log.split(" ")[1][0].isalpha()]
        digit_logs = [log for log in logs if log.split(" ")[1][0].isdigit()]

        def sort_key(x: str):
            index = x.find(" ")
            return (x[index + 1 :], x[:index])

        letter_logs.sort(key=sort_key)

        return letter_logs + digit_logs


s = Solution()

# Test case 1: Expecting ["let1 art can","let3 art zero","let2 own kit dig","dig1 8 1 5 1","dig2 3 6"]
# logs = [
#     "dig1 8 1 5 1",
#     "let1 art can",
#     "dig2 3 6",
#     "let2 own kit dig",
#     "let3 art zero",
# ]

# Test case 2: Expecting ["g1 act car","a8 act zoo","ab1 off key dog","a1 9 2 3 1","zo4 4 7"]
logs = ["a1 9 2 3 1", "g1 act car", "zo4 4 7", "ab1 off key dog", "a8 act zoo"]
result = s.reorderLogFiles(logs)
print(result)
