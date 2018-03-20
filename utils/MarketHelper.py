# -*- coding: utf-8 -*-
import sys,os
path=os.path.join(os.path.dirname(__file__),os.path.pardir)
sys.path.append(path)
from medium.Ticker import Ticker
from medium.Depth import Depth
from medium.Order import Order
from medium.UserInfo import UserInfo
from medium.K import K
from medium.KLine import KLine

#1min, 5min, 15min, 1day, 1week,,1
def formatPeriod(market,period):
    if market=='okex':
        return period
    elif market=='huobi':
        return period
    elif market=='zb':
        return period


def okexFromatTicker(symbol,json):
    ticker=Ticker()
    if "error_code" in json :
        order.setError(json['error_code'])
    else:
        ticker.setInfo(symbol,float(json['ticker']['last']),float(json['ticker']['sell']),float(json['ticker']['buy']),float(json['ticker']['vol']),"okex")
    return ticker

def okexFromatDepth(symbol,json):
    depth=Depth()
    if "error_code" in json :
        order.setError(json['error_code'])
    elif len(json['asks'])==0 or len(json['bids'])==0 :
        depth.setError()
    else:
        depth.setInfo(symbol,json['asks'],json['bids'],"okex")
    return depth

#status -1:已撤销  0:未成交  1:部分成交  2:完全成交 3:撤单处理中
def okexFromatOrder(symbol,json,classify,type="buy",price=0,amount=0):
    order_info=Order()
    if "error_code" in json :
        order_info.setError(json['error_code'])
        if classify=='order':
            order_info=[order_info]
    elif classify == 'trade':
        order_info.setInfo(symbol,json['order_id'],type,"未成交",price,0,amount,0,"okex")
    elif classify == 'order':
        order_info=[]
        for i in range(len(json['orders'])):
            order_temp=json['orders'][i]
            if order_temp['status']==-1:
                status='已撤销'
            elif order_temp['status']==0:
                status='未成交'
            elif order_temp['status']==1:
                status='部分成交'
            elif order_temp['status']==2:
                status='完全成交'
            elif order_temp['status']==3:
                status='撤单处理中'
            order=Order()
            order.setInfo(symbol,order_temp['order_id'],order_temp['type'],status,order_temp['price'],order_temp['avg_price'],order_temp['amount'],order_temp['deal_amount'],"okex")
            order_info.append(order)
    elif classify=='cancelOrder':
        order_info.setInfo(symbol,json['order_id'],None,'已撤销',0,0,0,0,"okex")
    return order_info

def okexFromatUserInfo(json):
    userinfo=UserInfo()
    if "error_code" in json :
        userinfo.setError(json['error_code'])
    else:
        free={}
        freezed={}
        for key,values in json['info']['funds']['free'].items():
            free[key]=float(values)
        for key,values in json['info']['funds']['freezed'].items():
            freezed[key]=float(values)
        userinfo.setInfo(free,freezed,"okex")       
    return userinfo

def okexFormatKLine(symbol,json):
    kline_array=[]
    kline=KLine()
    if "error_code" in json :
        kline.setError(json['error_code'])
    else:
        for item in json:
          k=K()
          k.setInfo(symbol,int(int(item[0])/1000),float(item[1]),float(item[2]),float(item[3]),float(item[4]),float(item[5]))
          k.setMarket('okex')
          kline_array.append(k)
        kline.setInfo(symbol,kline_array)
        kline.setMarket('okex')    
    return kline

def zbFormatKLine(symbol,json):
    kline_array=[]
    kline=KLine()
    if "error_code" in json :
        kline.setError(json['error_code'])
    else:
        for item in json["data"]:
          k=K()
          k.setInfo(symbol,int(int(item[0])/1000),float(item[1]),float(item[2]),float(item[3]),float(item[4]),float(item[5]))
          k.setMarket('zb')
          kline_array.append(k)
        kline.setInfo(symbol,kline_array)
        kline.setMarket('zb') 
    return kline

def huobiFormatKLine(symbol,json):
    kline_array=[]
    kline=KLine()
    if json["status"]=="error" :
        kline.setError('未知错误')
    else:
        for item in json["data"]:
          k=K()
          k.setInfo(symbol,int(item["id"]),float(item["open"]),float(item["high"]),float(item["low"]),float(item["close"]),float(item["vol"]))
          k.setMarket('huobi')
          kline_array.append(k)
        kline_array.reverse()
        kline.setInfo(symbol,kline_array)
        kline.setMarket('huobi')        
    return kline

def rechargeCoin(userInfo,free_amount=0,freezed_amount=0,**argv):
    for key in userInfo.free:
        if key in argv:
            userInfo.free[key]=argv[key]
        else:
            userInfo.free[key]=free_amount
    for key in userInfo.freezed:
        if key in argv:
            userInfo.freezed[key]=argv[key]
        else:
            userInfo.freezed[key]=freezed_amount
    return userInfo
    

          


if __name__ =='__main__':
    ticker=Ticker()

    print(ticker)
