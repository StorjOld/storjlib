import binascii
import hashlib
import storjlib
import partialhash
from pycoin.encoding import ripemd160


def valid_id(shardid):
    return storjlib.util.is_hex_hash(shardid)


def get_size(shard):
    """Get the size of a shard.

    Args:
        shard: A file like object representing the shard.

    Returns: The shard size in bytes.
    """
    shard.seek(0, 2)
    return shard.tell()


def get_hash_bin(shard, salt=b"", size=0, offset=0):
    """Get the hash of the shard.

    Args:
        shard: A file like object representing the shard.
        salt: Optional salt to add as a prefix before hashing.

    Returns: Hex digetst of ripemd160(sha256(salt + shard)).
    """

    shard.seek(0)
    digest = partialhash.compute(shard, offset=offset, length=size, seed=salt,
                                 hash_algorithm=hashlib.sha256)

    shard.seek(0)
    return ripemd160(digest).digest()


def get_hash_hex(shard, hex_salt="", size=0, offset=0):
    """Get the hash of the shard.

    Args:
        shard: A file like object representing the shard.
        hex_salt: Optional hex encoded salt to add as a prefix before hashing.
        size: TODO doc string
        offset: TODO doc string

    Returns: Hex digetst of ripemd160(sha256(salt + shard)).
    """
    salt = binascii.unhexlify(hex_salt) if hex_salt else ""
    return binascii.hexlify(get_hash_bin(shard, salt=salt,
                                         size=size, offset=offset))


def get_id(shard):
    """Returns the hex encoded hash of the shard"""
    return get_hash_hex(shard)


def copy(src_shard, dest_fobj):
    """Copy a shard to a file like object.

    Args:
        src_shard: A file like object representing the shard to copy.
        dest_fobj: A file like object to copy the shard to.
    """
    src_shard.seek(0)
    while True:
        data = src_shard.read(4096)
        if not data:
            break
        dest_fobj.write(data)


def save(shard, path):
    """Copy a shard to a file.

    Args:
        src_shard: A file like object representing the shard to copy.
        path: The path to save the shard at.
    """
    with open(path, "wb") as fobj:
        copy(shard, fobj)
