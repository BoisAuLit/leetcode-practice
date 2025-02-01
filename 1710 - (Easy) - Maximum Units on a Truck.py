from typing import List


class Solution:
    def maximumUnits(self, boxTypes: List[List[int]], truckSize: int) -> int:
        sorted_list = sorted(boxTypes, key=lambda x: x[1], reverse=True)
        result = 0
        index = 0
        while index < len(sorted_list):
            nb_boxes, units = sorted_list[index]
            if truckSize >= nb_boxes:
                result += nb_boxes * units
                truckSize -= nb_boxes
            else:
                result += truckSize * units
                break
            index += 1

        return result


s = Solution()

# Test case 1: Expecting 8
# boxTypes = [[1, 3], [2, 2], [3, 1]]
# truckSize = 4

# Test case 2: Expecting 91
boxTypes = [[5, 10], [2, 5], [4, 7], [3, 9]]
truckSize = 10

result = s.maximumUnits(boxTypes, truckSize)


print(result)
