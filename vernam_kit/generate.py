#!/usr/bin/env python

import sys
import os
from getpass import getpass
from hashlib import sha256
from operator import xor
from optparse import OptionParser
from functools import reduce

# py2-py3 compatibility
if isinstance(bytes([0]), str):
    int_to_byte = chr
else:
    int_to_byte = lambda x: bytes([x])


def sha_random_gen(init_data):
    """
    PRNG based on SHA-256
    :param user_input:
    :return:
    """
    # py2-py3 compatibility
    if hasattr(init_data, 'encode'):
        init_data = init_data.encode(sys.stdin.encoding)

    # py2-py3 compatibility
    data = sha256(init_data).digest()
    if isinstance(data, str):
        f = ord
    else:
        f = lambda _: _

    while True:
        for x in data:
            yield f(x)
        data = sha256(data).digest()


def urandom_gen():
    while True:
        yield ord(os.urandom(1))


def random_gen(*entropy_gen):
    while True:
        yield int_to_byte(reduce(xor, map(next, entropy_gen)))


def main(output, size, skip_user_input):
    generators = [
        urandom_gen(),
    ]
    if not skip_user_input:
        user_input = getpass('Presses any buttons on the keyboard:')
        generators.append(sha_random_gen(user_input))
    gen = random_gen(*generators)
    for _ in range(size):
        output.write(next(gen))


def endpoint():
    usage = "Usage: %prog [OPTIONS]"
    parser = OptionParser(usage)
    parser.add_option("-o", "--output", dest="output",
                      help="write one-time pad to FILE", metavar="FILE")
    parser.add_option("-s", "--size", dest="size", type="int",
                      help="one-time pad SIZE in bytes", metavar="SIZE")
    parser.add_option("-S", "--skip_user_input", dest="skip_user_input",
                      action="store_true",
                      help="Skip user input to generate random data")

    options, args = parser.parse_args()

    if not options.size:
        parser.error("size is required")

    if options.output:
        output = open(options.output, 'wb')
    else:
        # py2-py3 compatibility
        output = getattr(sys.stdout, 'buffer', sys.stdout)

    main(output, options.size, options.skip_user_input)

    if options.output:
        output.close()


if __name__ == '__main__':
    endpoint()
