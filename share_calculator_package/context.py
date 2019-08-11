import copy


def compensating_capital_gains(context):
    return context['capital_gains'] - context['sheltered_tax_fund']


def losses_to_cover(context):
    return context['capital_losses'] - compensating_capital_gains(context)


def sheltered_tax_fund_shortfall(context):
    return context['sheltered_tax_fund_target'] - context['sheltered_tax_fund']


def sell_shares(context, bucket_index, shares_to_sell):
    context = copy.deepcopy(context)
    bucket = context['buckets'][bucket_index]
    if bucket['cost_basis'] > context['share_price']:
        context['capital_losses'] += shares_to_sell * (bucket['cost_basis'] - context['share_price'])
    else:
        bucket_gains = shares_to_sell * (context['share_price'] - bucket['cost_basis'])
        context['capital_gains'] += bucket_gains
        context['sheltered_tax_fund'] += bucket_gains

    context['total_shares_to_sell'] += shares_to_sell
    bucket['quantity'] -= shares_to_sell
    return context
