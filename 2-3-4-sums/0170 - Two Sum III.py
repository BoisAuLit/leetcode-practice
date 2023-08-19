from collections import Counter


class TwoSum:
    def __init__(self):
        self.array = []
        self.counter = Counter()

    def add(self, number: int) -> None:
        self.array.append(number)
        self.counter.update({number: 1})

    def find(self, value: int) -> bool:
        if len(self.array) < 2:
            return False
        for v, count in self.counter.items():
            complement = value - v
            if v == complement:
                if count >= 2:
                    return True
            elif complement in self.counter:
                return True
        return False


s = TwoSum()
s.add(1)
s.add(3)
s.add(5)
result1 = s.find(4)
print(result1)
result2 = s.find(7)
print(result2)
