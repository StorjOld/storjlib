import math
import six
import re
import binascii
from pycoin.encoding import hash160


def hash_bin(data):
    """ripemd160(hashlib.sha256(data)"""
    return hash160(data)


def hash_hex(hexdata):
    """ripemd160(hashlib.sha256(hexdata)"""
    return binascii.hexlify(hash160(binascii.unhexlify(hexdata)))


def is_hex_hash(hexdata):
    pattern = r"^[0-9a-f]{40,40}$"
    return isinstance(hexdata, six.string_types) and re.match(pattern, hexdata)


def is_bin_hash(data):
    return isinstance(data, six.binary_type) and len(data) == 20


def next_power_of_two(n):
    return 1 << (n - 1).bit_length()


def perfect_binary_tree_depth(width):
    return int(math.log(width, 2))
