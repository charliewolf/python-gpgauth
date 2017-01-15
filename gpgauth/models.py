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
        return self.long_fingerprint == other.long_fingerprint
