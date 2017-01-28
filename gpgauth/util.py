import datetime
import enum
import random

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


class Random(random.Random):
    # Adapted from the stdlib. this gives deterministic behavior in python(2|3)
    def randbelow(self, max):
        "Return a random int in the range [0,n).  Raises ValueError if n==0."

        bits = max.bit_length()
        result = self.getrandbits(bits)
        while result >= max:
            result = self.getrandbits(bits)
        return result
