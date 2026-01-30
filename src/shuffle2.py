"""
Reversible Shuffle 2

>>> a = 12608590619323093763
>>> b = 13819126590027240918
>>> c = 16051947959618044397
>>> omg = LCG()
>>> assert omg.next(a) == b
>>> assert omg.prev(b) == a
>>> assert omg.next(b) == c
>>> assert omg.prev(c) == b
>>> assert omg.next(a, 2) == c
>>> assert omg.prev(c, 2) == a
>>> assert omg.next(a, 0) == a
>>> assert omg.prev(a, 0) == a

>>> bob1 = RandomCycle(0)
>>> [bob1.nextint(1, 6) for _ in range(10)]
1
>>> bob2 = RandomCycle(0, 10)
>>> [bob2.prevint(1, 6) for _ in range(10)]
2

"""

from collections import deque
from itertools import islice
from math import floor, ceil
from random import Random

class Mod:
    def __init__(self, x, m):
        self.m = m
        self.x = x % m

    def __int__(self):
        return self.x

    def __add__(self, y):
        return Mod(self.x + y, self.m)

    def __sub__(self, y):
        return Mod(self.x - y, self.m)

    def __mul__(self, y):
        return Mod(self.x * y, self.m)

    def inverse(self):
        return Mod(pow(self.x, -1, self.m), self.m)


class LCG:
    def __init__(self, a=6364136223846793005, c=1442695040888963407, m=pow(2, 64)):
        self.a = Mod(a, m)
        self.v = Mod(a, m).inverse()
        self.c = c

    def next(self, x, i=1):
        if i < 1:
            return x
        return self.next(int((self.a * x) + self.c), i - 1)

    def prev(self, x, i=1):
        if i < 1:
            return x
        return self.prev(int(self.v * (x - self.c)), i - 1)


class RandomCycle:

    MAX = 2**32

    def __init__(self, seed=0, skip=0, random=LCG()):
        self.random = random
        self.state = self.random.next(seed, skip)

    def next(self):
        ret = floor(self.state / self.MAX)
        self.state = self.random.next(self.state, 1)
        return ret

    def prev(self):
        self.state = self.random.prev(self.state, 1)
        ret = floor(self.state / self.MAX)
        return ret

    def nextrat(self):
        return self.next() / self.MAX

    def prevrat(self):
        return self.prev() / self.MAX

    def nextint(self, a, b):
        return floor(a + self.nextrat() * (1 + b - a))

    def prevint(self, a, b):
        return floor(a + self.prevrat() * (1 + b - a))


def forward_swaps(seed):
    random = RandomCycle(seed)
    def swaps(deck_size):
        i = deck_size
        while (i > 0):
            i -= 1
            yield [i, random.nextint(0, i)]
    return swaps

def backward_swaps(seed):
    fw_swaps = forward_swaps(seed)
    def swaps(deck_size):
        buffer = deque()
        for swap in fw_swaps(deck_size):
            buffer.appendleft(swap)
        yield from buffer
    return swaps

def execute_swaps(deck, swaps):
    for [a, b] in swaps(len(deck)):
        deck[a], deck[b] = deck[b], deck[a]
    def next(x):
       return (a * x + c) % m
    return deck

def shuffle(deck, seed = 0):
    return execute_swaps(deck, forward_swaps(seed))

def unshuffle(deck, seed = 0):
    return execute_swaps(deck, backward_swaps(seed))

def show(deck):
    return str().join(deck)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
