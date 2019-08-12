import itertools


def is_cross(bid_price, ask_price):
    return bid_price >= ask_price


def auction_match(bids, asks):
    it_bids = iter(bids)
    it_asks = iter(asks)

    bid = next(it_bids, None)
    ask = next(it_asks, None)

    exec_qty = 0
    exec_price = None

    if bid is None:
        return exec_price, exec_qty

    price = bid['price']

    while bid is not None and ask is not None:
        while not is_cross(bid["price"], ask["price"]):
            ask = next(it_asks, None)
            if ask is None:
                return exec_price, exec_qty

        qty = min(bid['qty'], ask['qty'])
        if qty > exec_qty:
            exec_price = price
            exec_qty = qty

        print({'price': price, 'qty': qty})

        next_bid = next(it_bids, None)
        next_ask = next(it_asks, None)
        if next_bid is None and next_ask is None:
            return exec_price, exec_qty
        elif next_bid is None:
            price = ask['price']
            ask = next_ask
            continue
        elif next_ask is None:
            price = bid['price']
            bid = next_bid
            continue

        if next_bid['price'] == next_ask['price']:
            bid = next_bid
            ask = next_ask
            price = bid['price']
        elif next_bid['price'] > next_ask['price']:
            bid = next_bid
            price = bid['price']
            it_asks = iter(list(itertools.chain([next_ask], it_asks)))
        else:
            ask = next_ask
            price = ask['price']
            it_bids = iter(list(itertools.chain([next_bid], it_bids)))

    return exec_price, exec_qty


def acc_list(l):
    qty = float(0)
    for x in l:
        qty += x['qty']
        x['qty'] = qty


def sort_and_acc_list(bids, asks):
    bids = sorted(bids, key=lambda x: x['price'], reverse=True)
    asks = sorted(asks, key=lambda x: x['price'])

    acc_list(bids)
    acc_list(asks)
    return bids, list(reversed(asks))


def main():
    bids = [
        {'price': 100, 'qty': 10},
        {'price': 101, 'qty': 15},
    ]
    asks = [
        {'price': 100, 'qty': 20},
        {'price': 101, 'qty': 5},
    ]

    x, y = sort_and_acc_list(bids, asks)
    print("Bids ----------------------")
    print(x)
    print("Asks ----------------------")
    print(y)

    price, qty = auction_match(x, y)
    print("Auction match: {}@{}".format(qty, price))


# main()
