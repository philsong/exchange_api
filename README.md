# jubi_api
聚币网API Python版本封装

# 使用

将`data.cfg.example`复制一份改名为`data.cfg`
聚币网申请`key`　将`public_key`和`private_key`填写在`data.cfg`中

# 文件说明

## jubi.py: api聚币网API
## jubi_get.py:抢购模式,用于抢购刚上市的币。
+ start_buy:间隔一秒轮询得到开盘信息。过滤掉卖单前几项(怕抢不到),按卖单价格挂单,把`self.buy_multi`注释打开
+ cancel_all:取消所有的买单和卖单
+ start_sell:根据当前币个数和自定义价格来卖出