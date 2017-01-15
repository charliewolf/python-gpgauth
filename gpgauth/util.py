import math
import datetime
import enum

RoundMode = enum.Enum('RoundMode', ('round', 'floor', 'ceil'))


def round_time(timestamp, resolution=datetime.timedelta(minutes=1), mode=RoundMode.round):

    round_to = resolution.total_seconds()

    seconds = (timestamp - timestamp.min).seconds

    if mode == RoundMode.ceil:
        # // is a floor division, not a comment on following line (like in javascript):
        rounding = (seconds + round_to) // round_to * round_to
    elif mode == RoundMode.floor:
        rounding = seconds // round_to * round_to
    elif mode == RoundMode.round:
        rounding = (seconds + round_to / 2) // round_to * round_to
    elif isinstance(mode, RoundMode):
        raise NotImplementedError(mode)
    else:
        raise ValueError("Invalid mode %s" % mode)

    return timestamp + datetime.timedelta(0, rounding - seconds, -timestamp.microsecond)


# Copying a couple randomizing functions here from the standard library because otherwise we don't get deterministic results (for unit tests) between python2 and python3
# The underlying `getrandbits` is deterministic, but `sample` and `randbelow` are not.

def sample(random, population, k):
        randbelow = _randbelow
        n = len(population)
        if not 0 <= k <= n:
            raise ValueError("Sample larger than population")
        result = [None] * k
        setsize = 21        # size of a small set minus size of an empty list
        if k > 5:
            setsize += 4 ** math.ceil(math.log(k * 3, 4))  # table size for big sets
        if n <= setsize:
            # An n-length list is smaller than a k-length set
            pool = list(population)
            for i in range(k):         # invariant:  non-selected at [0,n-i)
                j = randbelow(random, n-i)
                result[i] = pool[j]
                pool[j] = pool[n-i-1]   # move non-selected item into vacancy
        else:
            selected = set()
            selected_add = selected.add
            for i in range(k):
                j = randbelow(random, n)
                while j in selected:
                    j = randbelow(random, n)
                selected_add(j)
                result[i] = population[j]
        return result


def _randbelow(random, n):
        "Return a random int in the range [0,n).  Raises ValueError if n==0."

        getrandbits = random.getrandbits
        k = n.bit_length()  # don't use (n-1) here because n can be 1
        r = getrandbits(k)          # 0 <= r < 2**k
        while r >= n:
            r = getrandbits(k)
        return r
