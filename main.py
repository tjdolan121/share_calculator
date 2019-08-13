from context import *
from bucket import *

# ---------------------------------------
# Inputs

context = {
    'share_price': 4_000,
    'capital_gains': 500_000,
    'capital_losses': 0,
    'sheltered_tax_fund': 500_000,  # included in capital_gains as well
    'sheltered_tax_fund_target': 10_000_000,
    'sale_events_remaining': 4,
    'buckets': [
        {'cost_basis': 2_000, 'quantity': 1_000},
        {'cost_basis': 5_000, 'quantity': 4_000},
        {'cost_basis': 1_000, 'quantity': 50_000},
        {'cost_basis': 5_000, 'quantity': 8_000}
    ],
    'total_shares_to_sell': 0
}

# ----------------------------------------

print("--------------------------------------")
print(f"Initial position:\n\n"
      f"\tCapital Gains: ${context['capital_gains']/100:,}\n"
      f"\t\tSheltered Tax Fund: ${context['sheltered_tax_fund']/100:,}\n"
      f"\t\tSheltered Tax Fund Target: ${context['sheltered_tax_fund_target']/100:,}\n\n"
      f"\tCapital Losses: ${context['capital_losses']/100:,}\n\n"
      f"\tBuckets:")


for bucket in context['buckets']:
    print(f"\t\tAt ${bucket['cost_basis']/100:,} per share: {bucket['quantity']:,} shares owned")

i = 0

# This section gets you up to the sheltered tax fund target
while sheltered_tax_fund_shortfall(context) > 0 and i < 4:
    bucket_shares = shares_to_sell(context['buckets'][i], context, sheltered_tax_fund_shortfall(context))
    # calculate our losses or gains
    context = sell_shares(context, i, bucket_shares, initial_funding_reached=False)
    if context['buckets'][i]['quantity'] == 0:
        i += 1

# todo - handle the case where we can't get enough capital gains to balance our capital
#  losses (like tell the user or something)
# This section sells enough shares to cover for capital losses (assumes that there are
# some buckets left you can sell at a profit)

i = 0

while losses_to_cover(context) > 0 and i < 4:
    # calculate how many shares to sell
    bucket_shares = shares_to_sell(context['buckets'][i], context, losses_to_cover(context))

    # calculate losses or gains
    context = sell_shares(context, i, bucket_shares, initial_funding_reached=True)
    if context['buckets'][i]['quantity'] == 0:
        i += 1


print("--------------------------------------")
print(f"Ending position:\n\n"
      f"\tTotal Shares to Sell: {context['total_shares_to_sell']:,}\n"
      f"\t\tSell {int(context['total_shares_to_sell']) / int(context['sale_events_remaining'])} per event\n"
      f"\tCapital Gains: ${context['capital_gains']/100:,}\n"
      f"\t\tSheltered Tax Fund: ${context['sheltered_tax_fund']/100:,}\n"
      f"\t\tSheltered Tax Fund Target: ${context['sheltered_tax_fund_target']/100:,}\n\n"
      f"\tCapital Losses: ${context['capital_losses']/100:,}\n\n"
      f"\tBuckets:")


for bucket in context['buckets']:
    print(f"\t\tAt ${bucket['cost_basis']/100:,} per share: {bucket['quantity']:,} shares owned")
