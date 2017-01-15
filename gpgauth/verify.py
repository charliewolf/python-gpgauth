import datetime
import os
import tempfile
import gnupg

from gpgauth.exceptions import NoPublicKeyException, InvalidSignatureException, InvalidNonceException
from gpgauth.challenge import generate_challenge, generate_last_challenge
from gpgauth.models import GPGPublicKey


"""
    GPG 2nd-factor Web Authentication Utility Functions
    Site should present user with a challenge and reqest a signature generated with
        echo -n challenge | gpg --detach-sign --armor
    This is also time-verified.
"""


def verify_signature_for_challenges(signature, challenges, max_drift=90):
    gpg = gnupg.GPG()
    tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False, prefix='gpgauth')
    try:
        tmpfile.write(signature)
        tmpfile.close()
        verifications = [gpg.verify_data(data=challenge.encode('utf8'), sig_filename=tmpfile.name) for challenge in challenges]
    finally:
        os.remove(tmpfile.name)
    if any(verification.status == 'no public key' for verification in verifications):
        raise NoPublicKeyException(data=verifications)
    if all(verification.status != 'signature valid' for verification in verifications):
        raise InvalidSignatureException()
    valid_verification = [verification for verification in verifications if verification.status == 'signature valid'][0]
    signed_at = datetime.datetime.fromtimestamp(int(valid_verification.sig_timestamp))
    now = datetime.datetime.utcnow()
    nonce = abs((now - signed_at).total_seconds())
    if nonce > max_drift:
        raise InvalidNonceException(delta=datetime.timedelta(seconds=nonce), signed_at=signed_at, verified_at=now)
    return GPGPublicKey(fingerprint=valid_verification.pubkey_fingerprint)


def verify_signature(system_identifier, signature, max_drift=90):
    challenges = (generate_challenge(system_identifier=system_identifier), generate_last_challenge(system_identifier=system_identifier))
    return verify_signature_for_challenges(signature=signature, challenges=challenges, max_drift=max_drift)
