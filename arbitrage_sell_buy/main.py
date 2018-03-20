# -*- coding: utf-8 -*-
import sys,os,time,json
sys.path.append(os.path.join(os.path.dirname(__file__),os.path.pardir))

from medium.Order import Order
from market.Okex import Okex
from market.Zb import Zb
from market.HuoBi import HuoBi
from utils.EmailSender import EmailSender


def sendEmail(order):
  title=order.market+"_"+order.symbol
  info='币:{}_类型:{}_成交价格:{}_成交数量{}'.format(order.symbol,order.type,order.avg_price,order.deal_amount)
  emailSender.sendText(info,title)
  print('发送邮件{} {}'.format(title,info))

"""
功能：
1、检测市场上的订单状态。当订单状态从挂单转化为撤销或完全成交时，发一份邮件到手机里
逻辑：
1、order_ids 是当前市场上挂单的订单集合，通过遍历订单接口-未成交订单获取
2、diff_ids 上次挂单的订单集合  和本次遍历获取的订单集合的差集（上次有，本次没有的订单），即为已成交或撤销的订单。
3、miss_ids 在遍历 diff_ids 的订单信息。发生网络异常，加回到order_ids，用于下次验证
"""


if __name__=='__main__':
  
  env="release"
  with open(os.path.join(os.path.dirname(__file__),os.path.pardir,'config.json'),'r') as f:
      config=json.load(f)
  order_ids=set()
  emailSender=EmailSender(config["email"]["126"]["server"],config["email"]["126"]["username"],config["email"]["126"]["password"])

  with open(os.path.join(os.path.dirname(__file__),'coins.json'),'r') as f:
    coin_settings=json.load(f)
  with open(os.path.join(os.path.dirname(__file__),os.path.pardir,'config.json'),'r') as f:
    config=json.load(f)
  
  market_key=config[env]
  market_names=["okex","huobi","zb"]
  markets={"okex":Okex(market_key["okex"]["api_key"],market_key["okex"]["secret_key"]),"huobi":HuoBi(market_key["huobi"]["api_key"],market_key["huobi"]["secret_key"]),"zb":Zb(market_key["zb"]["api_key"],market_key["zb"]["secret_key"])}

  while True:
    temp_ids=set()
    for coin_setting in coin_settings:
      for market in market_names:
        if coin_setting[market]!=False:
          orders=markets[market].order(coin_setting["symbol"],-1)
          for i in range(len(orders)):
            order=orders[i]
            if order.status=="已撤销":
              pass
            elif order.status=="未成交":
              temp_ids.add("{},{},{}".format(market,order.symbol,order.id))
            elif order.status=="部分成交":
              temp_ids.add("{},{},{}".format(market,order.symbol,order.id))
            elif order.status=="完全成交":
              pass
            elif order.status=="撤单处理中":
              temp_ids.add("{},{},{}".format(market,order.symbol,order.id))
              pass
    #获取 order_ids有的而temp_ids没有的，即寻找已撤销或已成交的订单
    diff_ids=order_ids-temp_ids
    miss_ids=set()
    for order_str in diff_ids:
      order_info=order_str.split(",")
      orders=markets[order_info[0]].order(order_info[1],order_info[2])
      if orders[0].result==True:
        if orders[0].status=="已撤销":
          pass
        elif orders[0].status=="未成交":
          pass
        elif orders[0].status=="部分成交":
          pass
        elif orders[0].status=="完全成交":
          sendEmail(orders[0])
        elif orders[0].status=="撤单处理中":
          pass
      else:
        print("{}请求失败，等待下次请求".format(order_str))
        miss_ids.add(order_str)
    order_ids=temp_ids|miss_ids
    print('当前监控信息:')
    for order_str in order_ids:
      print(order_str)
    print('程序等待下一次循环')
    time.sleep(60)
  