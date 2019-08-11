from unittest import TestCase
from AuctionMatch import *


def log_bid_ask(bids, asks):
    print("Bids ----------------------")
    print(bids)
    print("Asks ----------------------")
    print(asks)


class TestAuction_match(TestCase):
    def setUp(self):
        self.bids = []
        self.asks = []
        self.expected_price = None
        self.expected_qty = 0.0
        print("Running {}...".format(self._testMethodName))

    def run_test(self):
        self.bids, self.asks = sort_and_acc_list(self.bids, self.asks)
        price, qty = auction_match(self.bids, self.asks)
        self.assertAlmostEqual(price, self.expected_price)
        self.assertAlmostEqual(qty, self.expected_qty)


    def test_simple_book(self):
        self.bids = [
            {'price': 100, 'qty': 10},
            {'price': 101, 'qty': 15},
        ]
        self.asks = [
            {'price': 100, 'qty': 20},
            {'price': 101, 'qty': 5},
        ]

        self.expected_price = 100.0
        self.expected_qty = 20.0

        self.run_test()

    def test_simple_book2(self):
        self.bids = [
            {'price': 100, 'qty': 10},
            {'price': 101, 'qty': 15},
        ]
        self.asks = [
            {'price': 100, 'qty': 5},
            {'price': 101, 'qty': 30},
        ]

        self.expected_price = 101.0
        self.expected_qty = 15.0

        self.run_test()

    def test_no_cross(self):
        self.bids = [
            {'price': 100, 'qty': 10}
        ]
        self.asks = [
            {'price': 101, 'qty': 5},
        ]

        self.expected_price = None
        self.expected_qty = 0.0

        self.run_test()

    def test_exact_one_cross(self):
        self.bids = [
            {'price': 100, 'qty': 30}
        ]
        self.asks = [
            {'price': 100, 'qty': 60}
        ]

        self.expected_price = 100
        self.expected_qty = 30

        self.run_test()

    def test_only_bids(self):
        self.bids = [
            {'price': 100, 'qty': 30}
        ]

        self.expected_price = None
        self.expected_qty = 0.0

        self.run_test()

    def test_only_asks(self):
        self.asks = [
            {'price': 100, 'qty': 30}
        ]

        self.expected_price = None
        self.expected_qty = 0.0

        self.run_test()

    def test_different_levels(self):
        self.bids = [
            {'price': 99.5, 'qty': 20},
            {'price': 100.0, 'qty': 25},
            {'price': 101.0, 'qty': 5}
        ]
        self.asks = [
            {'price': 99.6, 'qty': 25},
            {'price': 100.0, 'qty': 20},
            {'price': 101.0, 'qty': 30}
        ]

        self.expected_price = 100.0
        self.expected_qty = 30.0

        self.run_test()

    def test_different_levels_at_sub_level(self):
        self.bids = [
            {'price': 99.5, 'qty': 20},
            {'price': 100.0, 'qty': 25},
            {'price': 101.0, 'qty': 5}
        ]
        self.asks = [
            {'price': 99.6, 'qty': 55},
            {'price': 100.0, 'qty': 5},
            {'price': 101.0, 'qty': 10}
        ]

        self.expected_price = 100.0
        self.expected_qty = 30.0

        self.run_test()

    def test_different_levels_at_internal_sub_level(self):
        self.bids = [
            {'price': 100.0, 'qty': 20},
            {'price': 100.5, 'qty': 25},
            {'price': 101.0, 'qty': 5}
        ]
        self.asks = [
            {'price': 100.0, 'qty': 55},
            {'price': 100.6, 'qty': 5},
            {'price': 101.0, 'qty': 10}
        ]

        self.expected_price = 100.0
        self.expected_qty = 50

        self.run_test()

    def test_different_levels_first_ask(self):
        self.bids = [
            {'price': 99.0, 'qty': 20},
            {'price': 101.0, 'qty': 30}
        ]
        self.asks = [
            {'price': 100.0, 'qty': 15},
            {'price': 101.0, 'qty': 10},
            {'price': 101.5, 'qty': 20}
        ]

        self.expected_price = 101.0
        self.expected_qty = 25

        self.run_test()
