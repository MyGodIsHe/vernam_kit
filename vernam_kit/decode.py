#!/usr/bin/env python

import sys
import base64
from optparse import OptionParser
from operator import add
from functools import reduce


# py2-py3 compatibility
if isinstance(bytes([0]), str):
    int_to_byte = chr
    byte_to_int = ord
else:
    int_to_byte = lambda x: bytes([x])
    byte_to_int = lambda _: _


class BadSizePad(Exception):
    pass


def pop(f, size):
    f.seek(0, 2)
    tell = f.tell()
    if tell < size:
        raise BadSizePad
    f.seek(-size, 2)
    data = f.read()
    f.truncate(tell - size)
    return data


def main(cipher, pad, output):
    # py2-py3 compatibility
    if hasattr(cipher, 'decode'):
        cipher = cipher.decode(sys.stdin.encoding)

    cipher = base64.b64decode(cipher)
    gamma = pop(pad, len(cipher))

    plaintext = []
    for i, c in zip(cipher, gamma):
        plaintext.append(
            int_to_byte(
                byte_to_int(c) ^ byte_to_int(i)
            )
        )
    plaintext = reduce(add, plaintext)
    try:
        plaintext = plaintext.decode('utf-16be')
    except UnicodeDecodeError:
        pass
    output.write(plaintext.encode(sys.stdout.encoding))


def endpoint():
    usage = "Usage: %prog [OPTIONS] CIPHER_TEXT"
    parser = OptionParser(usage)
    parser.add_option("-o", "--output", dest="output",
                      help="write cipher to FILE", metavar="FILE")
    parser.add_option("-p", "--pad", dest="pad",
                      help="read one-time pad from FILE", metavar="FILE")

    options, args = parser.parse_args()

    if len(args) != 1:
        parser.error("incorrect number of arguments")

    if not options.pad:
        parser.error("pad is required")
    else:
        pad = open(options.pad, 'rb+')

    if options.output:
        output = open(options.output, 'wb')
    else:
        # py2-py3 compatibility
        output = getattr(sys.stdout, 'buffer', sys.stdout)

    try:
        main(args[0], pad, output)
    except BadSizePad:
        parser.error("insufficient size for one-time pad")
    finally:
        pad.close()
        if options.output:
            output.close()
        else:
            print('')


if __name__ == '__main__':
    endpoint()
