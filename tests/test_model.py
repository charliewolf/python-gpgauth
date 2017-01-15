import unittest

from gpgauth.models import GPGPublicKey


class ModelTest(unittest.TestCase):
    def test_public_key(self):
        public_key = GPGPublicKey(fingerprint="E0694D1A16020926AA7C6B9164586DEAD03E05B9")
        self.assertEqual(public_key.long_fingerprint, 'E0694D1A16020926AA7C6B9164586DEAD03E05B9')
        self.assertEqual(public_key.short_fingerprint, 'D03E05B9')
        self.assertEqual(str(public_key), 'D03E05B9')
        self.assertEqual(repr(public_key), 'GPGPublicKey<0xD03E05B9>')

    def test_public_keys_are_equal(self):
        public_key1 = GPGPublicKey(fingerprint="E0694D1A16020926AA7C6B9164586DEAD03E05B9")
        public_key2 = GPGPublicKey(fingerprint="E0694D1A16020926AA7C6B9164586DEAD03E05B9")
        self.assertEqual(public_key1, public_key2)
