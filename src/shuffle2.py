"""
Reversible Shuffle 2

Shuffles a list

>>> shuffle(list(range(8)))
[2, 7, 4, 5, 1, 0, 6, 3]

Unshuffles a list

>>> unshuffle([2, 7, 4, 5, 1, 0, 6, 3])
[0, 1, 2, 3, 4, 5, 6, 7]

Gives different shufflings based on seed

>>> show(shuffle(list('ELVIS'), 0x2050))
'LIVES'
>>> show(shuffle(list('ELVIS'), 0x1320))
'ILVES'

Unshuffles seeded shuffles

>>> show(unshuffle(list('LIVES'), 0x2050))
'ELVIS'
>>> show(unshuffle(list('ILVES'), 0x1320))
'ELVIS'

"""

from math import floor, ceil
from hashlib import sha512


def check_mod_arg(unsafe_f):
    def safe_f(self, arg, *args):
        if self.m != arg.m:
            raise TypeError
        return unsafe_f(self, arg, *args)
    return safe_f


class Mod:

    def __init__(self, x, m):
        self.x = x % m
        self.m = m

    def __repr__(self):
        return 'Mod(' + repr(self.x) + ', ' + repr(self.m) + ')'

    def __int__(self):
        return self.x

    def __contains__(self, arg):
        return Mod(arg, self.m) == self

    def __pow__(self, arg):
        return Mod(pow(self.x, arg, self.m), self.m)

    @check_mod_arg
    def __eq__(self, arg):
        return arg.x == self.x

    @check_mod_arg
    def __add__(self, arg):
        return Mod(self.x + arg.x, self.m)

    @check_mod_arg
    def __sub__(self, arg):
        return Mod(self.x - arg.x, self.m)

    @check_mod_arg
    def __mul__(self, arg):
        return Mod(self.x * arg.x, self.m)

    @check_mod_arg
    def __truediv__(self, arg):
        return Mod(self.x * pow(arg.x, -1, self.m), self.m)


class LCG:

    def __init__(self, size):
        self.size = size
        [a, c, m] = LCG._config(size)
        self.a = Mod(a, m)
        self.c = Mod(c, m)
        self.m = m

    def next(self, x, s = 1):
        tmp = Mod(x, self.m)
        for i in range(s):
            tmp = (self.a * tmp) + self.c
        return int(tmp)

    def prev(self, x, s = 1):
        tmp = Mod(x, self.m)
        for i in range(s):
            tmp = (tmp - self.c) / self.a
        return int(tmp)

    @staticmethod
    def _multiplier(size):
        match size:
            case 64:
                return 0xf9b25d65  # Steele–Vigna (2020)
        raise ValueError

    @staticmethod
    def _config(size):
        a = LCG._multiplier(size)
        c = 1
        m = 2 ** size
        return [a, c, m]


class Mixer:

    def __init__(self, _hash):
        self._hash = _hash

    def mix(self, x):
        return self._hash(x).digest()


class Random:

    def __init__(self, seed = 0, skip = 0, prng = LCG(64), mixer = Mixer(sha512)):
        self._prng = prng
        self._mixer = mixer
        seed_length = ceil(seed.bit_length() / 8)
        seed_bytes = seed.to_bytes(seed_length)
        init_bytes = mixer.mix(seed_bytes)
        init_value = int.from_bytes(init_bytes)
        self._state = self._prng.next(init_value, skip)

    def _next(self):
        buffer = self._state.to_bytes(self._prng.size)
        self._state = self._prng.next(self._state)
        return self._mixer.mix(buffer)

    def _prev(self):
        self._state = self._prng.prev(self._state)
        buffer = self._state.to_bytes(self._prng.size)
        return self._mixer.mix(buffer)

    def next_ratio(self):
        return self._ratio(self._next())

    def prev_ratio(self):
        return self._ratio(self._prev())

    def next_int(self, a, b):
        return a + floor(self.next_ratio() * (1 + b - a))

    def prev_int(self, a, b):
        return a + floor(self.prev_ratio() * (1 + b - a))

    @staticmethod
    def _ratio(buffer):
        value = int.from_bytes(buffer)
        byte_size = len(buffer)
        bit_size = byte_size * 8
        max_value = 2 ** bit_size
        return value / max_value


def forward_swaps(seed):
    def swaps(deck_size):
        random = Random(seed)
        i = deck_size
        while (i > 0):
            i -= 1
            yield [i, random.next_int(0, i)]
    return swaps

def backward_swaps(seed):
    def swaps(deck_size):
        random = Random(seed, deck_size)
        i = 0
        while (i < deck_size):
            yield [i, random.prev_int(0, i)]
            i += 1
    return swaps

def execute_swaps(deck, swaps):
    for [a, b] in swaps(len(deck)):
        deck[a], deck[b] = deck[b], deck[a]
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
