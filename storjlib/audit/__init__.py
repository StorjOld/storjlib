import storjlib


def _collapse_proof(proof, leaf, depth):

    if depth == 0:
        assert(len(proof) == 1)  # contains only the challenge response
        assert(storjlib.util.is_hex_hash(proof[0]))
        assert(storjlib.util.hash_hex(proof[0]) == leaf)  # for expected leaf
        return leaf

    assert(len(proof) == 2)

    # collapse left branch
    if isinstance(proof[0], list):
        hashl = _collapse_proof(proof[0], leaf, depth - 1)
    else:
        assert(storjlib.util.is_hex_hash(proof[0]))
        hashl = proof[0]  # end of branch

    # collapse right branch
    if isinstance(proof[1], list):
        hashr = _collapse_proof(proof[1], leaf, depth - 1)
    else:
        assert(storjlib.util.is_hex_hash(proof[1]))
        hashr = proof[1]  # end of branch

    return storjlib.util.hash_hex(hashl + hashr)


def validate(proof, root, challengenum, leaves):
    width = storjlib.util.next_power_of_two(len(leaves))
    depth = storjlib.util.perfect_binary_tree_depth(width)
    leaf = leaves[challengenum]
    try:
        return root == _collapse_proof(proof, leaf, depth)
    except AssertionError:
        return False  # incorrect proof format
