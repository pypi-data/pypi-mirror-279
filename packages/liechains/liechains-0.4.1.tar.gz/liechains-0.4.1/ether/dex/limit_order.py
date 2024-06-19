from ether.dex.swap import Swap
from concurrent.futures import ThreadPoolExecutor


def get_quotes(dexes: list[Swap], limit_price, min_amount, max_amount):
    """
    并发获取不同dex的报价
    return (dex, (amount, price))
    """
    dex_count = len(dexes)
    pool = ThreadPoolExecutor(dex_count)
    amount_threshould = (max_amount - min_amount) / 100
    quotes = pool.map(
        search_max_amount_on_dex,
        dexes,
        [min_amount] * dex_count,
        [max_amount] * dex_count,
        [limit_price] * dex_count,
        [amount_threshould] * dex_count,
        [0] * dex_count,
        [0] * dex_count,
    )
    return list(zip(dexes, quotes))


def search_max_amount_on_dex(
    dex: Swap,
    min_amount,
    max_amount,
    limit_price,
    amount_threshould,
    current_best_amount,
    current_price,
):
    # print(f'search on {min_amount} {max_amount} {current_best_amount} {current_price}')
    # 查找粒度足够小， 就返回最好的结果
    if max_amount - min_amount < amount_threshould:
        return current_best_amount, current_price

    mid_amount = (min_amount + max_amount) // 2
    amount_out = dex.quote(mid_amount)
    # print(mid_amount, amount_out)
    price = mid_amount / amount_out
    # 价格符合要求， 继续加量
    if price < limit_price:
        return search_max_amount_on_dex(
            dex,
            mid_amount,
            max_amount,
            limit_price,
            amount_threshould,
            mid_amount,
            price,
        )
    else:
        # 超出限价， 往回搜索
        return search_max_amount_on_dex(
            dex,
            min_amount,
            mid_amount,
            limit_price,
            amount_threshould,
            current_best_amount,
            current_price,
        )
