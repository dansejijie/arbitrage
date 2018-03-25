# -*- coding: utf-8 -*-
import sys,os,time,json
sys.path.append(os.path.join(os.path.dirname(__file__),os.path.pardir,os.path.pardir))

from medium.K import K
from medium.KLine import KLine
from market.Okex import Okex
from market.Zb import Zb
from market.HuoBi import HuoBi

def getIncreaseFallRatioArray(kline):
  start =0
  if len(kline) - 288 > 0:
    start=len(kline) - 288
  kline=kline.split(start,len(kline))
  for k in kline.kline:
    if (k.high-k.open)>(k.high-k.close):
      k.up_profit=(k.high-k.close)/k.close
    else :
      k.up_profit=(k.high-k.open)/k.open
    
    if (k.open-k.low)>(k.close-k.low):
      k.down_profit=(k.close-k.low)/k.low
    else :
      k.down_profit=(k.open-k.low)/k.low
  return kline


def findLimitIncreaseFallRatioData(kline,limit = 0.08):
  up_profit_num=0
  down_profit_num=0
  for k in kline.kline:
    if k.up_profit>limit:
      up_profit_num+=1
    if k.down_profit>limit:
      down_profit_num+=1
  kline.up_profit_num=up_profit_num
  kline.down_profit_num=down_profit_num
  return kline


"""
寻找买一价格在0.0040一下的币
"""
if __name__ =='__main__':
  market_array=["okex"]
  paths=[]
  markets=[]
  coins=[]
  for value in market_array:
    if value =='okex':
      markets.append(Okex('xx','xx'))
    elif value == 'zb':
      markets.append(Zb('xx','xx'))
    elif value =='huobi':
      markets.append(HuoBi('xx','xx'))
    else :
      print('未知市场')
    path=os.path.join(os.path.dirname(__file__),value+'.json')
    with open(path,'rt') as f:
      coins.append(json.load(f))
  
  for market_index,market_coins in enumerate(coins):
    market=markets[market_index]
    result=[]
    for coin in market_coins:
      ticker=market.ticker(coin)
      if ticker.result:
          print('计算{}中'.format(coin))
          if ticker.buy<0.004:
            result.append({"symbol":ticker.symbol,"buy":ticker.buy})
      else:
        print('coin:{} 请求网络失败:{}'.format(coin,ticker.message))
    print('{}市场开始写入'.format(market_array[market_index]))

    write_file=os.path.join(os.path.dirname(__file__),"record",market_array[market_index]+"_"+time.strftime('%Y-%m-%d')+'.txt')
    
    with open(write_file, 'w') as f:
      for r in result:
        f.write('{}\t{}\n'.format(r["symbol"],r["buy"]))
  print('完成')
  
  
      
      
      
