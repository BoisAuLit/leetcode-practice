from typing import List, Tuple

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    directions = {"N": (0, 1, "W", "E"), "S": (0, -1, "E", "W"), "W": (-1, 0, "S", "N"), "E": (1, 0, "N", "S")}

    def walk(self, direction: str, current_position: Tuple[int, int], instructions: List[str]):
        for step in instructions:
            if step == "G":
                x, y = Solution.directions[direction][0], Solution.directions[direction][1]
                current_position = (current_position[0] + x, current_position[1]+y)
            else:
                if step == "L":
                    direction = Solution.directions[direction][2]
                else:
                    direction = Solution.directions[direction][3]
        return direction, current_position

    def isRobotBounded(self, instructions: str) -> bool:
        direction = "N"
        current_position = (0, 0)
        for _ in range(4):
            direction, current_position = self.walk(direction, current_position, instructions)
            if current_position == (0, 0):
                return True

        return False


s = Solution()
input_ = "GGLLGG" # True
# input_ = "GG" # False
# input_ = "GL" # True

result = s.isRobotBounded(input_)
print(result)
