
def is_cross(bid_price, ask_price):
    return bid_price >= ask_price


def auction_match(bids, asks):
    it_bids = iter(bids)
    it_asks = iter(asks)
    # try:
    #     bid = bids[0]
    #     ask = asks[0]
    # except IndexError:
    #     return None, 0.0

    bid = next(it_bids, None)
    ask = next(it_asks, None)

    exec_qty = 0
    exec_price = None
    # not work
    # way = 'bid' if bid['price'] > ask['price'] else 'ask'
    way = 'bid'
    results = []

    while bid is not None and ask is not None:
        while not is_cross(bid["price"], ask["price"]):
            ask = next(it_asks, None)
            if ask is None:
                return exec_price, exec_qty

        price = bid['price'] if way is 'bid' else ask['price']
        # Cannot take min here, wrong!
        # price = min(bid['price'], ask['price'])
        if is_cross(bid["price"], ask["price"]):
            qty = min(bid['qty'], ask['qty'])
            if qty > exec_qty:
                exec_price = price
                exec_qty = qty
            results.append({'price': price, 'qty': qty})

        next_bid = next(it_bids, None)
        next_ask = next(it_asks, None)
        if next_bid is None and next_ask is None:
            break
        elif next_bid is None:
            next_bid = bid
        elif next_ask is None:
            next_ask = ask

        if next_bid['price'] == next_ask['price']:
            bid = next_bid
            ask = next_ask
        elif next_bid['price'] > next_ask['price']:
            way = 'bid'
            bid = next_bid
        else:
            way = 'ask'
            ask = next_ask

        # if is_cross(next_bid['price'], ask['price']):
        #     way = 'bid'
        #     bid = next_bid
        # else:
        #     way = 'ask'
        #     ask = next(it_asks, None)

    print('Results: {}'.format(results))
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
