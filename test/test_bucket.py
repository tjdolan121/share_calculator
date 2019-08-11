import unittest
from bucket import *


class TestBucket(unittest.TestCase):
    def test_total_shares(self):
        buckets = [
            {'cost_basis': 1000, 'quantity': 100},
            {'cost_basis': 500, 'quantity': 250}
        ]

        self.assertEqual(total_shares(buckets), 350)

    def test_value(self):
        bucket = {'cost_basis': 400, 'quantity': 250}

        self.assertEqual(value(bucket), 100000)

    def test_returns(self):
        bucket = {'cost_basis': 400, 'quantity': 100}
        share_price = 500

        self.assertEqual(returns(bucket, share_price), 10000)

    def test_shares_to_sell_sell_whole_bucket_at_a_loss(self):
        bucket = {'cost_basis': 100, 'quantity': 200}
        context = {'share_price': 90, 'sheltered_tax_fund_target': 40,
                   'sheltered_tax_fund': 30}

        self.assertEqual(shares_to_sell(bucket, context), 200)

    def test_shares_to_sell_sell_partial_bucket_at_a_gain(self):
        bucket = {'cost_basis': 100, 'quantity': 200}
        context = {'share_price': 200, 'sheltered_tax_fund_target': 400,
                   'sheltered_tax_fund': 300}

        self.assertEqual(shares_to_sell(bucket, context), 1)

    def test_shares_to_sell_sell_whole_bucket_at_a_gain(self):
        bucket = {'cost_basis': 100, 'quantity': 2}
        context = {'share_price': 200, 'sheltered_tax_fund_target': 600,
                   'sheltered_tax_fund': 300}

        self.assertEqual(shares_to_sell(bucket, context), 2)

    def test_shares_to_sell_sell_whole_bucket_at_a_gain_exact_target(self):
        bucket = {'cost_basis': 100, 'quantity': 3}
        context = {'share_price': 200, 'sheltered_tax_fund_target': 600,
                   'sheltered_tax_fund': 300}

        self.assertEqual(shares_to_sell(bucket, context), 3)
