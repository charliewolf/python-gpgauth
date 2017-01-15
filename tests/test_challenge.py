import unittest
import datetime

from gpgauth.challenge import generate_challenge, generate_last_challenge


class ChallengeTest(unittest.TestCase):
    def test_challenge_generator(self):
        timestamp = datetime.datetime(year=2017, month=1, day=1, hour=12)
        self.assertEqual(generate_challenge('test', timestamp=timestamp), 'joshua tahiti panama orient')

    def test_identifier_seeds(self):
        timestamp = datetime.datetime(year=2017, month=1, day=1, hour=12)
        self.assertEqual(generate_challenge('test', timestamp=timestamp), 'joshua tahiti panama orient')
        self.assertEqual(generate_challenge('test2', timestamp=timestamp), 'paprika pegasus tribune amazon')

    def test_custom_word_list(self):
        timestamp = datetime.datetime(year=2017, month=1, day=1, hour=12)
        self.assertEqual(generate_challenge('test', timestamp=timestamp, word_list='sometimes i love to write python code but other times it is literally the worst thing ever'.split()), 'worst is python i')

    def test_custom_word_count(self):
        timestamp = datetime.datetime(year=2017, month=1, day=1, hour=12)
        self.assertEqual(generate_challenge('test', timestamp=timestamp, num_words=8), 'joshua tahiti panama orient emotion juice metal wisdom')

    def test_rounding_works(self):
        timestamp1 = datetime.datetime(year=2017, month=1, day=1, hour=12, minute=1, second=0)
        timestamp2 = datetime.datetime(year=2017, month=1, day=1, hour=12, minute=3, second=0)
        timestamp3 = datetime.datetime(year=2017, month=1, day=1, hour=12, minute=4, second=20)
        print(timestamp1)
        print(timestamp2)
        print(timestamp3)
        self.assertEqual(generate_challenge('test', timestamp=timestamp1), 'joshua tahiti panama orient')
        self.assertEqual(generate_challenge('test', timestamp=timestamp2), 'joshua tahiti panama orient')
        self.assertEqual(generate_challenge('test', timestamp=timestamp3), 'joshua tahiti panama orient')

    def test_get_last(self):
        timestamp1 = datetime.datetime(year=2017, month=1, day=1, hour=12, minute=1, second=0)
        timestamp2 = datetime.datetime(year=2017, month=1, day=1, hour=12, minute=9, second=0)
        self.assertEqual(generate_challenge('test', timestamp=timestamp1), 'joshua tahiti panama orient')
        self.assertEqual(generate_last_challenge('test', timestamp=timestamp2), 'joshua tahiti panama orient')
        self.assertEqual(generate_challenge('test', timestamp=timestamp2), 'aurora metal comrade value')
