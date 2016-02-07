from storjlib import util


def collapse_proof(proof, leaf, depth):

    if depth == 0:
        assert(len(proof) == 1)  # contains only the challenge response
        assert(util.is_hex_hash(proof[0]))
        assert(util.hash_hex(proof[0]) == leaf)  # response for expected leaf
        return leaf

    assert(len(proof) == 2)

    # collapse left branch
    if isinstance(proof[0], list):
        hashl = collapse_proof(proof[0], leaf, depth - 1)
    else:
        assert(util.is_hex_hash(proof[0]))
        hashl = proof[0]  # end of branch

    # collapse right branch
    if isinstance(proof[1], list):
        hashr = collapse_proof(proof[1], leaf, depth - 1)
    else:
        assert(util.is_hex_hash(proof[1]))
        hashr = proof[1]  # end of branch

    return util.hash_hex(hashl + hashr)


def validate(proof, root, challengenum, leaves):
    width = util.next_power_of_two(len(leaves))
    depth = util.perfect_binary_tree_depth(width)
    leaf = leaves[challengenum]
    try:
        return root == collapse_proof(proof, leaf, depth)
    except AssertionError:
        return False  # incorrect proof or proof format
