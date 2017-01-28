import datetime

from gpgauth.util import round_time, Random
from gpgauth.constants import WORD_LIST, DEFAULT_RESOLUTION, NUM_WORDS


def generate_challenge(system_identifier, timestamp=None, resolution=DEFAULT_RESOLUTION, num_words=NUM_WORDS, word_list=WORD_LIST):
    if not timestamp:
        timestamp = datetime.datetime.utcnow()
    rounded_time = round_time(timestamp, resolution=resolution)
    identifier_seed = int(sum(map(ord, system_identifier)))
    epoch = datetime.datetime.utcfromtimestamp(0)
    time_seed = int((rounded_time - epoch).total_seconds())
    seed = time_seed + identifier_seed
    shuffler = Random()
    try:
        shuffler.seed(seed, version=1)
    except TypeError:
        shuffler.seed(seed)
    return " ".join([word_list[i] for i in (shuffler.randbelow(len(word_list)) for x in range(num_words))])


def generate_last_challenge(system_identifier, timestamp=None, resolution=DEFAULT_RESOLUTION, *args, **kwargs):
    if not timestamp:
        timestamp = datetime.datetime.utcnow()
    timestamp = timestamp - resolution
    return generate_challenge(system_identifier, timestamp, resolution, *args, **kwargs)
