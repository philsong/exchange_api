# -*- coding: utf-8 -*-
# @Author: wujiyu
# @Date:   2017-07-09 10:44:41
# @Last Modified by:   far
# @Last Modified time: 2017-07-25 09:28:12

from utils import *


BASE_API = "https://www.jubi.com/api/v1"

TICKER_API = "%s/ticker" % BASE_API
DEPTH_API = "%s/depth" % BASE_API
ORDERS_API = "%s/orders" % BASE_API
BALANCE_API = "%s/balance" % BASE_API
TRADLIST_API = "%s/trade_list" % BASE_API
TRADEVIEW_API = "%s/trade_view" % BASE_API
TRADECANCEL_API = "%s/trade_cancel" % BASE_API
TRADEADD_API = "%s/trade_add" % BASE_API


class JuBi(object):
    """docstring for JuBi"""

    def __init__(self):
        super(JuBi, self).__init__()
        cfg = getUserData('data.cfg')
        self.public_key = cfg['public_key']
        self.private_key = cfg['private_key']

    def get_ticker(self, coin):
        data_wrap = {'coin': coin}
        return http_get(TICKER_API, data_wrap, True)

    def get_depth(self, coin):
        data_wrap = {'coin': coin}
        return http_get(DEPTH_API, data_wrap, True)

    def get_orders(self, coin):
        data_wrap = {'coin': coin}
        return http_get(ORDERS_API, data_wrap, True)

    def get_balance(self):
        nonce = get_nonce_time()
        data_wrap = {'nonce': nonce,
                     'key': self.public_key}
        all_data = get_signature(self.private_key, data_wrap)
        return http_get(BALANCE_API, all_data)

    def get_trade_list(self, coin):
        #  open:正在挂单, all:所有挂单
        trade_type = "open"
        since = "0"
        nonce = get_nonce_time()
        data_wrap = {'nonce': nonce, 'type': trade_type, 'coin': coin, 'since': since,
                     'key': self.public_key}
        all_data = get_signature(self.private_key, data_wrap)
        return http_get(TRADLIST_API, all_data)

    def get_trade_view_list(self, coin, id):
        nonce = get_nonce_time()
        data_wrap = {'nonce': nonce, 'coin': coin,
                     'key': self.public_key, 'id': id}
        all_data = get_signature(self.private_key, data_wrap)
        return http_get(TRADEVIEW_API, all_data)

    def cancel(self, coin, id):
        nonce = get_nonce_time()
        data_wrap = {'nonce': nonce, 'coin': coin,
                     'key': self.public_key, 'id': id}
        all_data = get_signature(self.private_key, data_wrap)
        return http_get(TRADECANCEL_API, all_data)

    def trade_add(self, coin, amount, price, sell_type):
        nonce = get_nonce_time()
        data_wrap = {'nonce': nonce, 'coin': coin,
                     'key': self.public_key, 'amount': amount, "price": price, "type": sell_type}
        all_data = get_signature(self.private_key, data_wrap)
        return http_get(TRADEADD_API, all_data)

    def sell(self, coin, amount, price):
        return self.trade_add(coin, amount, price, "sell")

    def buy(self, coin, amount, price):
        return self.trade_add(coin, amount, price, "buy")

    def cancel_all(self, coin, sell_type="all"):
        lst = self.get_trade_list(coin)
        print("当前挂单!!!!!!!!!!:%s" % (lst))
        for item in lst:
            if sell_type == "all" or sell_type == item["type"]:
                self.cancel(coin, item["id"])
        print("取消挂单成功!!!!!!!!!")
        print("当前挂单!!!!!!!!!!:%s" % (self.get_trade_list(coin)))
        return True

    def cancel_all_sell(self, coin):
        return self.cancel_all(coin, "sell")

    def cancel_all_buy(self, coin):
        return self.cancel_all(coin, "buy")


# coin = "zcc"
# jubi = JuBi()
# print(jubi.get_ticker("coin))
# print(jubi.get_depth(coin))
# print(jubi.get_orders(coin))
# print(jubi.get_balance())
# print(jubi.get_trade_list(coin))
# print(jubi.get_trade_view_list(coin, "1"))
# print(jubi.get_trade_cancel_list(coin, "1"))
# print(jubi.sell(coin, 10000, 0.001))
# print(jubi.buy(coin, 100, 0.2))
# print(jubi.get_trade_cancel_list(coin, "1"))
# print(jubi.cancel(coin, 940591))
