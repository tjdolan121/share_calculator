import unittest
from context import *


class TestContext(unittest.TestCase):
    def test_compensating_capital_gains(self):
        context = {
            'capital_gains': 500,
            'sheltered_tax_fund': 300
        }

        self.assertEqual(compensating_capital_gains(context), 200)

    def test_losses_to_cover(self):
        context = {
            'capital_gains': 500,
            'sheltered_tax_fund': 300,
            'capital_losses': 300
        }

        self.assertEqual(losses_to_cover(context), 100)

    def test_opp_fund_shortfall(self):
        context = {
            'sheltered_tax_fund_target': 100,
            'sheltered_tax_fund': 50
        }

        self.assertEqual(sheltered_tax_fund_shortfall(context), 50)

    def test_sell_shares_at_a_gain_initial_funding_not_reached(self):
        context = {
            'buckets': [
                {'cost_basis': 100, 'quantity': 30}
            ],
            'capital_gains': 1000,
            'share_price': 200,
            'total_shares_to_sell': 0,
            'sheltered_tax_fund': 2000,
        }

        updated_context = sell_shares(context, 0, 10, initial_funding_reached=False)

        self.assertEqual(updated_context['buckets'][0]['quantity'], 20)
        self.assertEqual(updated_context['capital_gains'], 2000)
        self.assertEqual(updated_context['total_shares_to_sell'], 10)
        self.assertEqual(updated_context['sheltered_tax_fund'], 3000)

    def test_sell_shares_at_a_loss_initial_funding_not_reached(self):
        context = {
            'buckets': [
                {'cost_basis': 200, 'quantity': 30}
            ],
            'capital_losses': 1000,
            'share_price': 100,
            'total_shares_to_sell': 0,
        }

        updated_context = sell_shares(context, 0, 10, initial_funding_reached=False)

        self.assertEqual(updated_context['buckets'][0]['quantity'], 20)
        self.assertEqual(updated_context['capital_losses'], 2000)
        self.assertEqual(updated_context['total_shares_to_sell'], 10)

    def test_sell_shares_at_a_gain_initial_funding_reached(self):
        context = {
            'buckets': [
                {'cost_basis': 100, 'quantity': 30}
            ],
            'capital_gains': 1000,
            'share_price': 200,
            'total_shares_to_sell': 0,
            'sheltered_tax_fund': 2000,
        }

        updated_context = sell_shares(context, 0, 10, initial_funding_reached=True)

        self.assertEqual(updated_context['buckets'][0]['quantity'], 20)
        self.assertEqual(updated_context['capital_gains'], 2000)
        self.assertEqual(updated_context['total_shares_to_sell'], 10)
        self.assertEqual(updated_context['sheltered_tax_fund'], 2000)

    def test_sell_shares_at_a_loss_initial_funding_reached(self):
        context = {
            'buckets': [
                {'cost_basis': 200, 'quantity': 30}
            ],
            'capital_losses': 1000,
            'share_price': 100,
            'total_shares_to_sell': 0,
        }

        updated_context = sell_shares(context, 0, 10, initial_funding_reached=True)

        self.assertEqual(updated_context['buckets'][0]['quantity'], 20)
        self.assertEqual(updated_context['capital_losses'], 2000)
        self.assertEqual(updated_context['total_shares_to_sell'], 10)
