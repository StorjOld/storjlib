import apigen
from . contract import validate
from . version import __version__  # NOQA


class Storjlib(apigen.Definition):

    @apigen.command()
    def contract_validate(self, contract):
        return validate(contract)

    # @apigen.command()
    # def contract_is_complete(self, contract):
    #     raise NotImplementedError()

    # @apigen.command()
    # def contract_sign(self, contract, key):
    #     raise NotImplementedError()


if __name__ == "__main__":
    apigen.run(Storjlib)
