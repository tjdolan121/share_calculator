from context import *
from bucket import *

# ---------------------------------------
# Inputs

context = {
    'share_price': 4_000,
    'capital_gains': 0,
    'capital_losses': 0,
    'sheltered_tax_fund': 500_000,  # included in capital_gains as well
    'sheltered_tax_fund_target': 100_000_000,
    'sale_events_remaining': 4,
    'buckets': [
        {'cost_basis': 2_000, 'quantity': 10_000},
        {'cost_basis': 3_000, 'quantity': 4_000},
        {'cost_basis': 1_000, 'quantity': 6_000},
        {'cost_basis': 5_000, 'quantity': 8_000}
    ],
    'total_shares_to_sell': 0
}

# ----------------------------------------

losses = 0  # -> renamed this to capital_losses

gains = 0  # -> renamed this to capital_gains

i = 0

shares_sold = 0  # -> renamed to shares_to_sell

# This section gets you up to the sheltered tax fund target
while sheltered_tax_fund_shortfall(context) > 0 and i < 4:
    bucket_shares = shares_to_sell(context['buckets'][i], context)
    # calculate our losses or gains
    context = sell_shares(context, i, bucket_shares)
    if context['buckets'][i]['quantity'] == 0:
        i += 1

# todo - handle the case where we can't get enough capital gains to balance our capital losses (like tell the user or someting)
# This section sells enough shares to cover for capital losses (assumes that there are some buckets left you can sell at a profit)
while losses_to_cover(context) > 0 and i < 4:
    # calculate how many shares to sell
    if buckets[i][0] < SHARE_PRICE and losses_to_cover(context) < buckets[i][1] * (
            SHARE_PRICE - buckets[i][0]):  # only need to sell part of the bucket
        bucket_shares = losses_to_cover(context) / (SHARE_PRICE - buckets[i][0])
    else:  # sell whole bucket (if its at a loss, or you need to sell this whole bucket and then some)
        bucket_shares = buckets[i][1]

    # calculate losses or gains
    if buckets[i][0] > SHARE_PRICE:
        bucket_losses = bucket_shares * (buckets[i][0] - SHARE_PRICE)
        losses += bucket_losses
    else:
        bucket_gains = bucket_shares * (SHARE_PRICE - buckets[i][0])
        gains += bucket_gains

    # update state
    shares_sold += bucket_shares
    buckets[i][1] -= bucket_shares
    i += 1

print(f"sell this many shares per sale event: {shares_sold / sale_events_remaining}")

# so many different ways to do string interpolation :)

print(f"i: {i}")
print(f"shares_sold: {shares_sold}")
print(f"losses: {losses / 100}")
print("gains: ", gains / 100)
print("sheltered_tax_fund: {}".format(sheltered_tax_fund / 100))
print("compensating capital gains: ", compensating_capital_gains(context) / 100)
