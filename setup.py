from __future__ import print_function
import sys
import setuptools

blacklist = ('register', 'upload')

for command in blacklist:
    if command in sys.argv:
        print('Command "%s" has been blacklisted, exiting.' % command, file=sys.stderr)
        sys.exit(2)

requirements = ["python-gnupg"]

if sys.version_info[:2] < (3, 4):
    requirements.append("enum34")

setuptools.setup(name='gpgauth', version='0.1', packages=('gpgauth',), install_requires=requirements)
