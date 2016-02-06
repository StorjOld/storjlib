import unittest
import storjlib


EXAMPLE_CONTRACT = {
    "type": "56ce3e837f575827cb5a94e2b609756a48fa4a3882f5e762b262af31f432878d",
    "renter_id": None,
    "renter_address": "240.0.0.1",
    "renter_port": 12345,
    "renter_signature": None,
    "farmer_id": None,
    "farmer_address": "240.0.0.2",
    "farmer_port": 12345,
    "farmer_signature": None,
    "data_size": 1234,
    "data_hash": None,
    "store_begin": 2000000000,
    "store_duration": 1000000000,
    "store_end": 3000000000,
    "audit_algorithm": "default",
    "audit_count": 10,
    "heartbeat_algorithm": "default",
    "heartbeat_count": 3600,
    "heartbeat_coverage": 12,
    "payment_currency": "SJCX",
    "payment_amount": 0,
    "payment_download_price": 0,
    "payment_destination": "1HtBKxEWpnAQpTd7URKmniW6afeKTzQDwY",
    "payment_source": "1DNYsfZBe5ajKkRnpMmqDQSaNuqc6Yxw95",
    "payment_begin": 2000000000,
    "payment_settlements": 0,
    "payment_interval": 0
}


class TestIsValid(unittest.TestCase):

    def test_example(self):
        api = storjlib.api.Storjlib()
        self.assertTrue(api.contract_is_valid(EXAMPLE_CONTRACT))


class TestIsComplete(unittest.TestCase):

    def test_something(self):
        pass


class TestSign(unittest.TestCase):

    def test_something(self):
        pass


if __name__ == "__main__":
    unittest.main()
