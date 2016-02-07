import six
import apigen
import storjlib
from . version import __version__  # NOQA


class Storjlib(apigen.Definition):

    @apigen.command()
    def contract_validate(self, contract):
        # TODO validate input
        return storjlib.contract.validate(contract)

    # @apigen.command()
    # def contract_is_complete(self, contract):
    #     raise NotImplementedError()

    # @apigen.command()
    # def contract_sign(self, contract, key):
    #     raise NotImplementedError()

    @apigen.command()
    def audit_validate(self, proof, root, challengenum, leaves):

        # validate input
        assert(isinstance(proof, list))
        assert(storjlib.util.is_hex_hash(root))
        assert(isinstance(leaves, list))
        for leaf in leaves:
            assert(storjlib.util.is_hex_hash(leaf))
        assert(isinstance(challengenum, six.integer_types))
        assert(0 <= challengenum < len(leaves))

        return storjlib.audit.validate(proof, root, challengenum, leaves)


if __name__ == "__main__":
    apigen.run(Storjlib)
