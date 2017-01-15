class GPGPublicKey(object):
    def __init__(self, fingerprint):
        self._fingerprint = fingerprint

    @property
    def long_fingerprint(self):
        return self._fingerprint

    @property
    def short_fingerprint(self):
        return self._fingerprint[-8:]

    def __str__(self):
        return self.short_fingerprint

    def __repr__(self):
        return "GPGPublicKey<0x%s>" % self.short_fingerprint

    def __eq__(self, other):
        if isinstance(other, GPGPublicKey):
            return self.long_fingerprint == other.long_fingerprint
        else:
            try:
                if other.startswith('0x'):
                    other = other[2:]
                if len(other) == 8:
                    return self.short_fingerprint == other
                else:
                    return self.long_fingerprint == other
            except AttributeError:
                raise TypeError("Can't compare with %s" % other)
