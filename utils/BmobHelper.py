# -*- coding: utf-8 -*-
import sys,os,json
path=os.path.join(os.path.dirname(__file__),os.path.pardir)
sys.path.append(path)
from medium.K import K
from medium.KLine import KLine
from bmob.Bmob import Bmob

"""
symbol:要获取的货币对
days:要获取的天数
"""
def getKLines(bmob,symbol,days=1):
  #天转化成15minK线要多少根
  minute_15=days*24*4
  result=bmob.queryArray(symbol,"-date",minute_15)
  if result.result==False:
    return result
  else:
    okex_array=[]
    huobi_array=[]
    zb_array=[]
    for i in range(len(result.extra)):
      item=result.extra[i]
      okex_k=K()
      okex_k.setInfo(symbol,item["date"],item["okex_open"],item["okex_high"],item["okex_low"],item["okex_close"],item["okex_vol"])
      okex_k.setMarket("okex")
      okex_array.append(okex_k)

      huobi_k=K()
      huobi_k.setInfo(symbol,item["date"],item["huobi_open"],item["huobi_high"],item["huobi_low"],item["huobi_close"],item["huobi_vol"])
      huobi_k.setMarket("huobi")
      huobi_array.append(huobi_k)

      zb_k=K()
      zb_k.setInfo(symbol,item["date"],item["zb_open"],item["zb_high"],item["zb_low"],item["zb_close"],item["zb_vol"])
      zb_k.setMarket("zb")
      zb_array.append(zb_k)
    
    okex_kline=KLine()
    okex_kline.setInfo(symbol,okex_array)
    okex_kline.setMarket("okex")
    huobi_kline=KLine()
    huobi_kline.setInfo(symbol,huobi_array)
    huobi_kline.setMarket("huobi")
    zb_kline=KLine()
    zb_kline.setInfo(symbol,zb_array)
    zb_kline.setMarket("zb")

    return [okex_kline,huobi_kline,zb_kline]

#返回的是数组
def getKLinesArray(bmob,symbol,days=1):
  #天转化成15minK线要多少根
  minute_15=days*24*4
  result=bmob.queryArray(symbol,"-date",minute_15)
  if result.result==False:
    return result
  else:
    okex_array=[]
    huobi_array=[]
    zb_array=[]
    for i in range(len(result.extra)):
      item=result.extra[i]
      okex_array.append({
        "date":item["date"],
        "open":item["okex_open"],
        "high":item["okex_high"],
        "low":item["okex_low"],
        "close":item["okex_close"],
        "vol":item["okex_vol"]
      })
      huobi_array.append({
        "date":item["date"],
        "open":item["huobi_open"],
        "high":item["huobi_high"],
        "low":item["huobi_low"],
        "close":item["huobi_close"],
        "vol":item["huobi_vol"]
      })
      zb_array.append({
        "date":item["date"],
        "open":item["zb_open"],
        "high":item["zb_high"],
        "low":item["zb_low"],
        "close":item["zb_close"],
        "vol":item["zb_vol"]
      })
    return {"okex":okex_array,"huobi":huobi_array,"zb":zb_array}

if __name__=='__main__':
  with open(os.path.join(os.path.dirname(__file__),os.path.pardir,'config.json'),'r') as f:
    config=json.load(f)
  bmob=Bmob(config["bmob"]["coin"]["api_key"],config["bmob"]["coin"]["secret_key"])

  #test 获取klines 内含对象
  klines=getKLines(bmob,"btc_usdt")
  print('xx')