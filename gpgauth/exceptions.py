class AuthException(Exception):
    pass


class InvalidSignatureException(AuthException):
    pass


class InvalidNonceException(AuthException):
    def __init__(self, delta, signed_at, verified_at):
        super(InvalidNonceException, self).__init__()
        self.delta = delta
        self.verified_at = verified_at
        self.signed_at = signed_at


class NoPublicKeyException(AuthException):
    def __init__(self, data):
        super(NoPublicKeyException, self).__init__()
        self.data = data
