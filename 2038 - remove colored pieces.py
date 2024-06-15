"""
Time complexity: O(n)
Space complexity: O(1)
"""


class Solution:
    def winnerOfGame(self, colors: str) -> bool:
        acc = alice = bob = 0
        last = colors[0]
        for letter in colors:
            if letter == last:
                acc += 1
            else:
                if acc >= 3:
                    if last == "A":
                        alice += acc - 2
                    else:
                        bob += acc - 2
                acc = 1

            last = letter
        if acc >= 3:
            if last == "A":
                alice += acc - 2
            else:
                bob += acc - 2
        return alice > bob


s = Solution()
input_ = "ABBBBBBBAAA"
result = s.winnerOfGame(input_)
print(result)
