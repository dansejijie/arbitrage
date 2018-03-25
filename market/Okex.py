
# -*- coding: utf-8 -*-
import sys,os,json
path=os.path.join(os.path.dirname(__file__),os.path.pardir)
sys.path.append(path)

import requests
import hashlib

from market.MarketClient import MarketClient
from utils.MarketHelper import okexFromatTicker,okexFromatDepth,okexFromatOrder,okexFromatUserInfo,okexFormatKLine,formatPeriod
from medium.Ticker import Ticker
from medium.Depth import Depth
from medium.Order import Order
from medium.UserInfo import UserInfo
from medium.KLine import KLine
ticker_url = "https://www.okex.com/api/v1/ticker.do?symbol="
userinfo_url = "https://www.okex.com/api/v1/userinfo.do"
order_url = "https://www.okex.com/api/v1/order_info.do"
cancel_order_url="https://www.okex.com/api/v1/cancel_order.do"
trade_url="https://www.okex.com/api/v1/trade.do"
depth_url="https://www.okex.com/api/v1/depth.do?symbol="
kline_url="https://www.okex.com/api/v1/kline.do?symbol="

class Okex(MarketClient):
    
    def __init__(self,api_key,secret_key):
        MarketClient.__init__(self,api_key,secret_key)

    def ticker(self,symbol,timeout=10):
        url=ticker_url+symbol
        try:
            r=requests.get(url,timeout=timeout)
            r=r.json()
            return okexFromatTicker(symbol,r)
        except Exception as e:
            ticker=Ticker()
            ticker.setError(e.args[0])
            return ticker

    def kline(self,symbol,type='15min',timeout=10):
        type=formatPeriod("okex",type)
        url=kline_url+symbol+'&type='+type
        try:
            r=requests.get(url,timeout=timeout)
            r=r.json()
            return okexFormatKLine(symbol,r)
        except Exception as e:
            kline=KLine()
            kline.setError(e.args[0])
            return kline

    def depth(self,symbol,size=50,timeout=10):
        url=depth_url+symbol+'&size='+str(size)
        try:
            r=requests.get(url,timeout=timeout)
            r=r.json()
            return okexFromatDepth(symbol,r)
        except Exception as e:
            depth=Depth()
            depth.setError(e.args[0])
            depth.symbol=symbol
            return depth
    def trade(self,symbol,price,amount,type,timeout=10):
        if type=="sell_market":
            sign="amount="+amount+"&api_key=" + self.api_key  + "&symbol=" + symbol +"&type=" +type+"&secret_key=" + self.secret_key
        elif type=="buy_market":
            sign="api_key=" + self.api_key + "&price=" + price + "&symbol=" + symbol +"&type=" +type+"&secret_key=" + self.secret_key
        else:
            sign = "amount="+str(amount)+"&api_key=" + self.api_key + "&price=" + str(price) + "&symbol=" + symbol +"&type=" +type+"&secret_key=" + self.secret_key;
        
        md5=hashlib.md5()
        md5.update(sign.encode("utf8"))
        sign=md5.hexdigest().upper()
        data={
            "amount":amount,
            "api_key": self.api_key,
            "price": price,
            "symbol": symbol,
            "type":type,
            "sign": sign
        }
        try:
            r=requests.post(trade_url,data,timeout=timeout)
            return okexFromatOrder(symbol,r.json(),"trade",type=type,price=price,amount=amount)
        except Exception as e:
            order=Order()
            order.setError(e.args[0])
            return order

    #argv [order,]
    def order(self,symbol,order_id,timeout=10):
        sign = "api_key=" + self.api_key + "&order_id=" + str(order_id) + "&symbol=" + symbol + "&secret_key=" + self.secret_key;
        md5=hashlib.md5()
        md5.update(sign.encode("utf8"))
        sign=md5.hexdigest().upper()
        data={
            "api_key": self.api_key,
            "order_id": order_id,
            "symbol": symbol,
            "sign": sign
        }
        try:
            r=requests.post(order_url,data,timeout=timeout)
            return okexFromatOrder(symbol,r.json(),"order")
        except Exception as e:
            order=Order()
            order.setError(e.args[0])
            return [order]
    def cancelOrder(self,symbol,order_id,timeout=10):
        sign = "api_key=" + self.api_key + "&order_id=" + str(order_id) + "&symbol=" + symbol + "&secret_key=" + self.secret_key;
        md5=hashlib.md5()
        md5.update(sign.encode("utf8"))
        sign=md5.hexdigest().upper()
        data={
            "api_key": self.api_key,
            "order_id": order_id,
            "symbol": symbol,
            "sign": sign
        }
        try:
            r=requests.post(cancel_order_url,data,timeout=timeout)
            return okexFromatOrder(symbol,r.json(),"cancelOrder")
        except Exception as e:
            order=Order()
            order.setError(e.args[0])
            return order
    def userinfo(self,timeout=10):
        sign = "api_key=" + self.api_key + "&secret_key=" + self.secret_key
        md5=hashlib.md5()
        md5.update(sign.encode("utf8"))
        sign=md5.hexdigest().upper()
        data={
            "api_key": self.api_key,
            "sign": sign
        }
        try:
            r=requests.post(userinfo_url,data,timeout=timeout)
            return okexFromatUserInfo(r.json())
        except Exception as e:
            user=UserInfo()
            user.setError(e.args[0])
            return user
#test
if __name__ == "__main__":

    with open(os.path.join(os.path.dirname(__file__),os.path.pardir,'config.json'),'r') as f:
        config=json.load(f)
    market=Okex(config["release"]["okex"]["api_key"],config["release"]["okex"]["secret_key"])

    #test ticker
    # ticker=market.ticker("btc_usdt")
    # print(ticker)

    #test depth
    depth=market.depth("show_usdt")
    print(depth)

    # test order
    # order=market.trade("light_usdt",0.001,100,"buy")
    # order=market.order("light_usdt",1949643,10)
    # print(order)

    #test cancel order
    # order=market.trade("cmt_usdt",0.1,100,"buy")
    # order=market.cancelOrder("cmt_usdt",order.id,order=order)
    # print(order)

    #test userinfo
    #user=market.userinfo()

    #test kline
    # kline=market.kline("ltc_btc")
    # print(kline[1])
    print('ok')






