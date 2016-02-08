import json
import jsonschema
import binascii
import btctxstore
from storjlib import util
from . schema import CONTRACT_SCHEMA


def validate(contract):
    try:
        jsonschema.validate(contract, CONTRACT_SCHEMA)
        return True
    except jsonschema.exceptions.ValidationError:
        return False


def _is_filled(contract, exclude=None):
    if exclude is not None:
        for key in exclude:
            assert(key in contract.keys())
    for key, value in contract.items():
        if exclude is not None and key in exclude:
            continue
        if value is None:
            return False
    return True


def _generate_signature_message(contract):
    message_fields = contract.copy()
    del message_fields["farmer_signature"]
    del message_fields["renter_signature"]
    return json.dumps(message_fields, sort_keys=True)


def sign(contract, key):

    _btcapi = btctxstore.BtcTxStore()

    # must be a valid contract
    validate(contract)

    # everything but signatures must be given
    exclude = ["farmer_signature", "renter_signature"]
    assert(_is_filled(contract, exclude=exclude))

    # key must be wif or hwif
    wif = None
    if _btcapi.validate_wallet(key):  # hwif given
        wif = _btcapi.get_key(key)
    elif _btcapi.validate_key(key):  # wif given
        wif = key
    assert(wif is not None)  # key is not wif or hwif
    btc_address = _btcapi.get_address(wif)

    # signing key must be from farmer or renter
    hexnodeid = binascii.hexlify(util.address_to_nodeid(btc_address))
    assert(hexnodeid in [contract["farmer_id"], contract["renter_id"]])

    # sign contract
    message = _generate_signature_message(contract)
    signature = _btcapi.sign_unicode(wif, message)

    # add signature to contract
    sigfield = None
    if contract["renter_id"] == hexnodeid:
        sigfield = "renter_signature"
    elif contract["farmer_id"] == hexnodeid:
        sigfield = "farmer_signature"
    assert(sigfield is not None)  # impossable state
    contract[sigfield] = signature

    return contract


def is_complete(contract):

    # Must be valid
    validate(contract)

    # All fields must be filled
    if not _is_filled(contract):
        return False

    # TODO check other things that need to be logically correct

    # check duration
    duration = contract["store_duration"]
    begin = contract["store_begin"]
    end = contract["store_end"]
    if end - begin != duration:
        return False

    # check signatures
    _btcapi = btctxstore.BtcTxStore()
    message = _generate_signature_message(contract)
    renter_btc_address = util.hexnodeid_to_address(contract["renter_id"])
    farmer_btc_address = util.hexnodeid_to_address(contract["farmer_id"])
    if not _btcapi.verify_signature_unicode(renter_btc_address,
                                            contract["renter_signature"],
                                            message):
        return False  # invalid renter signature
    if not _btcapi.verify_signature_unicode(farmer_btc_address,
                                            contract["farmer_signature"],
                                            message):
        return False  # invalid renter signature

    return True
