import context as cm


def total_shares(buckets):
    return sum([bucket['quantity'] for bucket in buckets])


def value(bucket):
    return bucket['quantity'] * bucket['cost_basis']


def returns(bucket, share_price):
    return (share_price - bucket['cost_basis']) * bucket['quantity']


def shares_to_sell(bucket, context):
    if bucket['cost_basis'] < context['share_price'] and \
            cm.sheltered_tax_fund_shortfall(context) < returns(bucket, context['share_price']):
        return cm.sheltered_tax_fund_shortfall(context) / (context['share_price'] - bucket['cost_basis'])
    else:
        return bucket['quantity']
