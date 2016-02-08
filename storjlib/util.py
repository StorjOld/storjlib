import math
import six
import re
import binascii
import os
import btctxstore
import decimal
import psutil
from pycoin.encoding import hash160
from pycoin.encoding import a2b_hashed_base58, b2a_hashed_base58


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


def address_to_nodeid(address):
    """Convert a bitcoin address to a node id."""
    return a2b_hashed_base58(address)[1:]


def address_to_hexnodeid(address):
    """Convert a bitcoin address to a hex node id."""
    return binascii.hexlify(address_to_nodeid(address))


def nodeid_to_address(nodeid):
    """Convert a node id to a bitcoin address."""
    return b2a_hashed_base58(b'\0' + nodeid)


def hexnodeid_to_address(hexnodeid):
    """Convert a hex node id to a bitcoin address."""
    return nodeid_to_address(binascii.unhexlify(hexnodeid))


def chunks(items, size):
    """ Split list into chunks of the given size.
    Original order is preserved.

    Example:
        > chunks([1,2,3,4,5,6,7,8,9], 2)
        [[1, 2], [3, 4], [5, 6], [7, 8], [9]]
    """
    return [items[i:i+size] for i in range(0, len(items), size)]


def baskets(items, count):
    """ Place list itmes in list with given basket count.
    Original order is not preserved.

    Example:
        > baskets([1,2,3,4,5,6,7,8, 9, 10], 3)
        [[1, 4, 7, 10], [2, 5, 8], [3, 6, 9]]
    """
    _baskets = [[] for _ in range(count)]
    for i, item in enumerate(items):
        _baskets[i % count].append(item)
    return list(filter(None, _baskets))


def ensure_path_exists(path):
    """Creates need directories if they do not already exist."""
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path):
        msg = "Creating path {0} failed!"  # pragma: no cover
        raise Exception(msg.format(path))  # pragma: no cover


def full_path(path):
    """Resolves, sym links, rel paths, variables, and tilds to abs paths."""
    prefix = "/" if path.startswith("/") else ""
    normalized = prefix + os.path.join(*re.findall(r"[^\\|^/]+", path))
    return os.path.abspath(os.path.expandvars(os.path.expanduser(normalized)))


def validate_positive_integer(i):
    if i < 0:
        msg = "Value must be greater then 0!"
        raise btctxstore.exceptions.InvalidInput(msg)
    return i


def byte_count(bc):  # ugly but much faster and safer then regex

    # default value or python api used
    if isinstance(bc, six.integer_types):
        return validate_positive_integer(bc)

    bc = btctxstore.deserialize.unicode_str(bc)

    def _get_byte_count(postfix, base, exponant):
        char_num = len(postfix)
        if bc[-char_num:] == postfix:
            count = decimal.Decimal(bc[:-char_num])  # remove postfix
            base = decimal.Decimal(base)
            exponant = decimal.Decimal(exponant)
            return validate_positive_integer(int(count * (base ** exponant)))
        return None

    # check base 1024
    if len(bc) > 1:
        n = None
        n = n if n is not None else _get_byte_count('K', 1024, 1)
        n = n if n is not None else _get_byte_count('M', 1024, 2)
        n = n if n is not None else _get_byte_count('G', 1024, 3)
        n = n if n is not None else _get_byte_count('T', 1024, 4)
        n = n if n is not None else _get_byte_count('P', 1024, 5)
        if n is not None:
            return n

    # check base 1000
    if len(bc) > 2:
        n = None
        n = n if n is not None else _get_byte_count('KB', 1000, 1)
        n = n if n is not None else _get_byte_count('MB', 1000, 2)
        n = n if n is not None else _get_byte_count('GB', 1000, 3)
        n = n if n is not None else _get_byte_count('TB', 1000, 4)
        n = n if n is not None else _get_byte_count('PB', 1000, 5)
        if n is not None:
            return n

    return validate_positive_integer(int(bc))


def get_free_space(dirname):
    """Return folder/drive free space (in bytes)."""
    return psutil.disk_usage(dirname).free


def get_folder_size(start_path):  # source http://stackoverflow.com/a/1392549
    """Returns the total size of all files in a directory."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def get_fs_type(path):
    """Returns: path filesystem type or None.

    Example:
        > get_fs_type("/home")
        'ext4'
    """
    partitions = {}
    for partition in psutil.disk_partitions():
        partitions[partition.mountpoint] = (partition.fstype,
                                            partition.device)
    if path in partitions:
        return partitions[path][0]
    splitpath = path.split(os.sep)
    for i in range(len(splitpath), 0, -1):
        subpath = os.sep.join(splitpath[:i]) + os.sep
        if subpath in partitions:
            return partitions[subpath][0]
        subpath = os.sep.join(splitpath[:i])
        if subpath in partitions:
            return partitions[subpath][0]
    return None
