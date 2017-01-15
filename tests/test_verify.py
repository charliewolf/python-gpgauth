import datetime
import textwrap
import unittest

from gpgauth.verify import verify_signature_for_challenges
from gpgauth.exceptions import InvalidNonceException, InvalidSignatureException


correct_horse_signature = textwrap.dedent("""
    -----BEGIN PGP SIGNATURE-----
    iQEzBAABCAAdFiEE4GlNGhYCCSaqfGuRZFht6tA+BbkFAlh67WsACgkQZFht6tA+
    Bbk62wf8DzFfNEHIIAgY083nqA1rVCIeaD8AxvHRjzNTvy37o9TOQ24MQPDdi+IH
    Hb0NFeJmW8lLynpwDdNaazcLCbWbA8gCMoQMCO1/ZyKECKT4lYlCWo2PF0GP2a69
    vkV/gSddLi7qLrSFhnYNknR07yrqJhNNcjDudcesxa50ba/IAdyPWdn0RSOn2Iah
    l9QdjZKQV5L82ouMCmB6bEzdwgAADAk9ageiGeARRmyIGiTa0CShL/m3BkaUB5s1
    GHtFQzXlBNxaWEzGo6r3EPxDNzZ8IaBPex+fIVxUCpCxijrMZxGcvxOHMVycj39E
    K0mSC5F2uQMTHCjI66zQbNbAmn75jg==
    =QGqh
    -----END PGP SIGNATURE-----
""").strip()


class VerificationTest(unittest.TestCase):

    def test_verification(self):
        challenge = 'correct horse battery staple'
        signature = correct_horse_signature
        public_key = verify_signature_for_challenges(challenges=(challenge,), signature=signature, max_drift=float('inf'))
        self.assertEqual(str(public_key), 'D03E05B9')

    def test_nonce(self):
        challenge = 'correct horse battery staple'
        signature = correct_horse_signature
        with self.assertRaises(InvalidNonceException):
            try:
                verify_signature_for_challenges(challenges=(challenge,), signature=signature, max_drift=1)
            except InvalidNonceException as exc:
                self.assertEqual(exc.signed_at, datetime.datetime(2017, 1, 14, 21, 32, 59))
                self.assertTrue(abs((exc.verified_at - datetime.datetime.utcnow()).total_seconds()) < 5)
                raise

    def test_signature_doesnt_match_challenge(self):
        challenge = 'correct horse laughs at you'
        signature = correct_horse_signature
        with self.assertRaises(InvalidSignatureException):
            verify_signature_for_challenges(challenges=(challenge,), signature=signature, max_drift=1)

    def test_invalid_signature_for_challenges(self):
        challenge = 'correct horse battery staple'
        signature = textwrap.dedent("""
                -----BEGIN PGP SIGNATURE-----
                iQEzBAABCAAdFiEE4GlNGhYCCSaqfGuRZFht6tA+BbkFAlh67WsACgkQZFht6tA+
                Bbk62wf8DzFfNEHIIAgY083nqA1rVCIeaD8AxvHRjzNTvy37o9TOQ24MQPDdi+IH
                Hb0NFeJmW8lLynpwDdNaazcLCbWbA8gCMoQMCO1/ZyKECKT4lYlCWo2PF0GP2a69
                vkV/gSddLi7qLrSFhnYNknR07ylqJhNNcjDudcesxa50ba/IAdyPWdn0RSOn2Iah
                l9QdjZKQV5L82ouMCmB6bEzdwgAADAk9ageiGeARRmyIGiTa0CShL/m3BkaUB5s1
                GHtFQzXlBNxaWEzGo6r3EPxDNzZ8IaBPex+fIVxUCpCxijrMZxGcvxOHMVycj39E
                K0mSC5F2uQMTHCjI66zQbNbAmn75jg==
                =QGqh
                -----END PGP SIGNATURE-----""").strip()
        with self.assertRaises(InvalidSignatureException):
            verify_signature_for_challenges(challenges=(challenge,), signature=signature)

    def test_corrupt_signature_for_challenges(self):
        challenge = 'correct horse battery staple'
        signature = 'sick horse bro'
        with self.assertRaises(InvalidSignatureException):
            verify_signature_for_challenges(challenges=(challenge,), signature=signature)

    def test_verification_multiple_challenges(self):
        challenge = 'correct horse battery staple'
        signature = correct_horse_signature
        public_key = verify_signature_for_challenges(challenges=("new challenge", challenge), signature=signature, max_drift=float('inf'))
        self.assertEqual(str(public_key), 'D03E05B9')

    def test_verification_multiple_challenges_reverse_order(self):
        challenge = 'correct horse battery staple'
        signature = correct_horse_signature
        public_key = verify_signature_for_challenges(challenges=(challenge, "new challenge"), signature=signature, max_drift=float('inf'))
        self.assertEqual(str(public_key), 'D03E05B9')

    def test_verification_multiple_challenges_all_wrong(self):
        signature = correct_horse_signature
        with self.assertRaises(InvalidSignatureException):
            verify_signature_for_challenges(challenges=("foo bar", "new challenge"), signature=signature, max_drift=float('inf'))
