import six
import apigen
import storjlib
from . version import __version__  # NOQA


class Storjlib(apigen.Definition):

    def __init__(self, quiet=False, debug=False, verbose=False, noisy=False,
                 config=storjlib.common.CONFIG_PATH):
        if isinstance(config, dict):
            storjlib.config.validate(config)
            self._cfg = config
        else:
            self._cfg = storjlib.config.get(path=config)

    @apigen.command()
    def contract_validate(self, contract):
        # TODO validate input
        return storjlib.contract.validate(contract)

    @apigen.command()
    def contract_sign(self, contract, key):
        # TODO validate input
        return storjlib.contract.sign(contract, key)

    @apigen.command()
    def contract_is_complete(self, contract):
        # TODO validate input
        return storjlib.contract.is_complete(contract)

    @apigen.command()
    def audit_validate(self, proof, root, challengenum, leaves):
        """ Validate an audit proof is for a given root and challange.

        Args:
            proof: The proof to be validated.
            root: The merkle root the proof must be for.
            challengenum: The leaf the proof must be for.
            leaves: All audit leaves (to ensure proof is not for other leaves).

        Retruns:
            True if the proof is correct.
        """

        # validate input
        assert(isinstance(proof, list))
        assert(storjlib.util.is_hex_hash(root))
        assert(isinstance(leaves, list))
        for leaf in leaves:
            assert(storjlib.util.is_hex_hash(leaf))
        assert(isinstance(challengenum, six.integer_types))
        assert(0 <= challengenum < len(leaves))

        return storjlib.audit.validate(proof, root, challengenum, leaves)

    @apigen.command()
    def audit_perform(self, shardid, leaves, challenge):
        # TODO validate input
        shard = storjlib.store.manager.open(self._cfg["storage"], shardid)
        return storjlib.audit.perform(shard, leaves, challenge)

    @apigen.command()
    def audit_prepare(self, shardid, challenges):
        # TODO validate input
        shard = storjlib.store.manager.open(self._cfg["storage"], shardid)
        return storjlib.audit.prepare(shard, challenges)

    @apigen.command()
    def store_import(self, paths):
        raise NotImplementedError()

    @apigen.command()
    def store_export(self, shardid, path):
        raise NotImplementedError()

    @apigen.command()
    def store_add(self, shard_path):
        # TODO validate input
        shard = open(storjlib.util.full_path(shard_path), "rb")
        storjlib.store.manager.add(self._cfg["storage"], shard)
        return storjlib.store.shard.get_id(shard)

    @apigen.command()
    def store_remove(self, shardid):
        # TODO validate input
        storjlib.store.manager.remove(self._cfg["storage"], shardid)


if __name__ == "__main__":
    apigen.run(Storjlib)
