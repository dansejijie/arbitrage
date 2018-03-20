# -*- coding: utf-8 -*-

import sys,os,time,json
sys.path.append(os.path.join(os.path.dirname(__file__),os.path.pardir))
from medium.Medium import Medium
from medium.K import K
from medium.KLine import KLine
from market.Okex import Okex
from market.Zb import Zb
from market.HuoBi import HuoBi
from bmob.Bmob import Bmob

"""
获取K线
"""
def getKLines(symbol_setting,period):
  klines=[]
  for market in market_symbol:
    if symbol_setting[market]==True:
        klines.append(markets[market].kline(symbol_setting["symbol"],period))
  return klines

def getSameLines(Klines,start_date,end_date):
  newklines=[]
  for i in range(len(klines)):
    newklines.append(getSameLine(klines[i],start_date,end_date))
  return newklines

"""
剪切两边，补充缺失K线
"""
def getSameLine(kline,start_date,end_date):
  increment=900
  newKline_array=[]
  for i in range(len(kline)):
    if kline[i].date>start_date and kline[i].date<=end_date:
      newKline_array.append(kline[i])
      #n 不为最后一个的时候
      if i+2<=len(kline):
        diff=kline[i+1].date-kline[i].date
        if diff>increment:
          diff_num=int(diff/increment)
          for j in range(1,diff_num):
            date=start_date+i*increment+j*increment
            k=K()
            k.setInfo(kline.symbol,date,kline[i].open,kline[i].high,kline[i].low,kline[i].close,kline[i].vol)
            k.setMarket(kline.market)
            newKline_array.append(k)
  kline.setInfo(kline.symbol,newKline_array)
  return kline
        
def getStartAndEndDate(klines):
  max_start_date=0
  min_end_date=float("inf")
  for i in range(len(klines)):
    if klines[i][0].date>max_start_date:
      max_start_date=klines[i][0].date
    if klines[i][-1].date<min_end_date:
      min_end_date=klines[i][-1].date
  return max_start_date,min_end_date

def judgeklines(klines):
  medium=Medium()
  for i in range(len(klines)):
    if klines[i].result==False:
      medium.setError(klines[i].message)
      break
  return medium
  
def transBmobKline(klines):
  newKLines=[]
  i=0
  while True:
    try:
      temp={}
      for j in range(len(klines)):
        temp["date"]=klines[j][i].date
        temp["{}_open".format(klines[j].market)]=klines[j][i].open
        temp["{}_high".format(klines[j].market)]=klines[j][i].high
        temp["{}_low".format(klines[j].market)]=klines[j][i].low
        temp["{}_close".format(klines[j].market)]=klines[j][i].close
        temp["{}_vol".format(klines[j].market)]=klines[j][i].vol
      newKLines.append(temp)
      i+=1
    except Exception as e:
      break
  return newKLines

def startHandleEvent():

  for symbol_setting in coins_settings:
    print('开始处理{}'.format(symbol_setting["symbol"]))
    search_date=None
    result=bmob.queryArrayByLimit(symbol_setting["symbol"],"-date",1,0)
    if len(result.extra)>0:
      search_date=result.extra[0]["date"]
    klines=getKLines(symbol_setting,"15min")
    result=judgeklines(klines)
    if result.result==True:
      start_date,end_date=getStartAndEndDate(klines)
      if search_date!=None and search_date>start_date:
        start_date=search_date
      klines=getSameLines(klines,start_date,end_date)
      newLines=transBmobKline(klines)
      print('{}正在上传Bmob数据库中'.format(symbol_setting["symbol"]))
      result=bmob.insertArray(symbol_setting["symbol"],newLines)
      if result.result==False:
        print('{}上传到Bmob数据库发生失败{}'.format(symbol_setting["symbol"],result.message))
    else:
      print(result.message)

if __name__ == '__main__':
  
    with open(os.path.join(os.path.dirname(__file__),os.path.pardir,'config.json'),'r') as f:
      config=json.load(f)
    bmob=Bmob(config["bmob"]["coin"]["api_key"],config["bmob"]["coin"]["secret_key"])
    market_symbol=["okex","huobi","zb"]
    markets={"okex":Okex('xx','xx'),"huobi":HuoBi('xx','xx'),"zb":Zb('xx','xx')}
    
    coin_path=os.path.join(os.path.dirname(__file__),'coins.json')
    with open(coin_path,'rt') as f:
      coins_settings=json.load(f)

    while True:
      startHandleEvent()
      time.sleep(1810)
      print('程序等待下一次执行中')
    print('程序退出循环')
    #klines=getKLines(symbol,"15min")