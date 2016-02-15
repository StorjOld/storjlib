from storjlib import util
from storjlib import store


def validate(proof, root, challengenum, leaves):
    """ Validate an audit proof is for a given root and challange.

    Args:
        proof: The proof to be validated.
        root: The merkle root the proof must be for.
        challengenum: The leaf the proof must be for.
        leaves: All audit leaves (to ensure proof is not for other leaves).

    Retruns:
        True if the proof is correct.
    """
    width = util.next_power_of_two(len(leaves))
    depth = util.perfect_binary_tree_depth(width)
    leaf = leaves[challengenum]
    try:
        return root == collapse(proof, leaf, depth)
    except AssertionError:
        return False  # incorrect proof or proof format


def perform(shard, leaves, seed, size=0, offset=0):
    response = store.shard.get_hash_hex(shard, hex_salt=seed,
                                        size=size, offset=offset)
    leaf = util.hash_hex(response)
    assert(leaf in leaves)
    challengenum = leaves.index(leaf)
    width = util.next_power_of_two(len(leaves))
    proof = leaves + [util.hash_hex("") for x in range(width - len(leaves))]
    proof[challengenum] = [response]
    return trim(proof, challengenum)


def trim(proof, index):
    """ Trim branches not leading to proof.
    Args:
        proof: The proof to be trimmed.
        index: Index of the branch to preserve, others are trimmed.

    Returns:
        The trimmed proof.
    """
    if len(proof) == 2:
        return proof
    proof = util.chunks(proof, 2)
    proof_next = []
    for branch_index, branch in enumerate(proof):
        if branch_index != index / 2:  # trim branch not leading to response
            proof_next.append(util.hash_hex(branch[0] + branch[1]))
        else:
            proof_next.append(branch)
    return trim(proof_next, index / 2)  # FIXME check it floors division!!!


def collapse(proof, leaf, depth):
    """ Collapse and validate the proof for the given leaf.

    Args:
        proof: The merkle proof to collapse.
        leaf: The leaf the given proof is for.
        depth: The reqired depth of the proof.

    Returns:
        The merkle root if the proof is valid.

    Raises:
        AssertionError: If incorrect proof or incorrect proof format.
    """

    if depth == 0:
        assert(len(proof) == 1)  # contains only the challenge response
        assert(util.is_hex_hash(proof[0]))
        assert(util.hash_hex(proof[0]) == leaf)  # response for expected leaf
        return leaf

    assert(len(proof) == 2)

    # collapse left branch
    if isinstance(proof[0], list):
        hashl = collapse(proof[0], leaf, depth - 1)
    else:
        assert(util.is_hex_hash(proof[0]))
        hashl = proof[0]  # end of branch

    # collapse right branch
    if isinstance(proof[1], list):
        hashr = collapse(proof[1], leaf, depth - 1)
    else:
        assert(util.is_hex_hash(proof[1]))
        hashr = proof[1]  # end of branch

    return util.hash_hex(hashl + hashr)


def prepare(shard, challenges):
    leaves = []
    # very inefficient implementation
    for challenge in challenges:
        seed = challenge["seed"]
        # FIXME use size and offset
        # size = challenge["size"]
        # offset = challenge["offset"]
        response = store.shard.get_hash_hex(shard, hex_salt=seed)
        leaves.append(util.hash_hex(response))
    return leaves
