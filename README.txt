gpgauth: a python library for GPG-based challenge/response 2-factor authentication

---
Overview:

    In addition to username and password, users will be asked to sign an arbitrary challenge, i.e.:
        echo -n correct horse battery staple | gpg --detach-sign --armor

    The resulting signature is verified against their account. If it was signed by a key associated with that user, they are allowed to log in.

    For organizations already implementing GPG and/or GPG smart cards, it is a natural way to piggyback 2fa off that.


Usage: The only functions a typical app will need are gpgauth.verify_signature and gpgauth.generate_challenge. See the sample_app directory for a full example.

