import apigen
# from . contract import is_valid
from . version import __version__  # NOQA


class Storjterms(apigen.Definition):

    @apigen.command()
    def contract_is_valid(self, contract):
        return False
        # return is_valid(contract)

    # @apigen.command()
    # def contract_is_complete(self, contract):
    #     raise NotImplementedError()

    # @apigen.command()
    # def contract_sign(self, contract, key):
    #     raise NotImplementedError()


if __name__ == "__main__":
    apigen.run(Storjterms)
