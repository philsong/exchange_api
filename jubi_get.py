# -*- coding: utf-8 -*-
# @Author: wujiyu
# @Date:   2017-07-09 16:15:50
# @Last Modified by:   wujiyu
# @Last Modified time: 2017-07-25 09:37:32

#  !!!!!!!!!!测试前先确定是否要开始抢购，别高价买了其他的币!!!!!!!!
from jubi import JuBi
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# coin = "zcc"
coin = "ugt"
interval = 1


class JuBiGet(object):
    """docstring for JuBiGet"""

    def __init__(self):
        super(JuBiGet, self).__init__()
        self.jubi = JuBi()

    def start_buy(self):
        player_info = self.jubi.get_balance()
        cny = player_info.cny_balance
        print("登录成功,当前余额:%s" % cny)
        print("获取牌价")
        ticker = self.jubi.get_ticker(coin)
        while ticker.volume == 0:
            print("还未开盘轮询%s秒获取" % interval)
            time.sleep(interval)
            ticker = self.jubi.get_ticker(coin)
            pass

        (has_asks, asks_lst) = self.get_market()
        while has_asks is False:
            time.sleep(interval)
            (has_asks, asks_lst) = self.get_market()
            pass

        #  !!!!!!!!!!测试前先确定是否要开始抢购，别高价买了其他的币!!!!!!!!
        # self.buy_multi(cny, asks_lst)

    def buy_multi(self, c_cny, asks_lst):
        for item in asks_lst:
            price = item[0]
            amount = item[1]
            # price = 0.1
            # amount = 10000

            buy_amount = amount
            if price * amount > c_cny:
                buy_amount = int(c_cny / price)
                if buy_amount < 1:
                    print("没钱了,不要买了!!!!!!!")
                    break

            buy_ret = self.jubi.buy(coin, buy_amount, price)
            if buy_ret.result is True:
                print("挂单成功,订单id:%s,价格:%s,数量:%s" % (buy_ret.id, price, buy_amount))
            c_cny = c_cny - buy_amount * price
            pass

    def get_market(self):
        print("获取市场挂单信息")
        market = self.jubi.get_depth(coin)

        bids_count = 0
        asks_count = 0
        if len(market.bids) > 0:
            for item in market.bids:
                if bids_count > 3:
                    break
                bids_count = bids_count + 1
                print("买单:%s" % item)

        print("")
        #  卖单按降序排一下,把最底出价单放前面
        asks_lst = market.asks[::-1]
        has_asks = len(asks_lst) > 0
        if has_asks:
            for item in asks_lst:
                if asks_count > 5:
                    break
                asks_count = asks_count + 1
                print("卖单:%s" % item)

        return (has_asks, asks_lst)

    def cancel_all(self):
        self.jubi.cancel_all(coin)

    def start_sell(self, price):
        player_info = self.jubi.get_balance()
        coin_balance = getattr(player_info, "%s_balance" % coin)
        print("登录成功,当前%s币个数:%s" % (coin, coin_balance))
        if coin_balance < 1:
            print("一个币都没有你卖个毛")
            return
        self.jubi.sell(coin, coin_balance, price)


if __name__ == '__main__':
    jubi_get = JuBiGet()
    #  抢购新币
    jubi_get.start_buy()
    # 取消所有挂单
    # jubi_get.cancel_all()
    #  出售价格
    # sell_price = 4
    # jubi_get.start_sell(sell_price)
