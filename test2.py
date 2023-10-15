from collections import UserDict


class MyDict(UserDict):
    def __add__(self, other):
        self.data.update(other)
        return self

    def __sub__(self, other):
        for key in other:
            if key in self.data:
                self.data.pop(key)
        return self


d1 = MyDict({1: 'a', 2: 'b'})
d2 = MyDict({3: 'c', 4: 'd'})
d5 = MyDict({6: 'c', 4: 'd'})

d3 = d1 + d2
print(d3)   # {1: 'a', 2: 'b', 3: 'c', 4: 'd'}

d4 = d3 - d5
print(d4)   # {1: 'a', 2: 'b'}