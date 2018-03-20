# -*- coding: utf-8 -*-

import sys,os,time,json
sys.path.append(os.path.join(os.path.dirname(__file__),os.path.pardir,os.path.pardir))

from medium.K import K
from medium.KLine import KLine
from market.Okex import Okex
from market.Zb import Zb
from market.HuoBi import HuoBi


"""
补齐K线
"""
def supplementKLine(kline,period):
  if period == '1min':
    increment=60
  elif period =='15min':
    increment=900
  elif period == '1day':
    increment=86400
  else:
    print('{} {}出现未知周期:supplementKLine 无法执行'.format(kline.market,kline.symbol))
    return
  kline_array=[]
  num=int((kline[-1].date-kline[0].date)/increment+1)
  start=kline[0].date

  supplement_num=0
  kline_num=0
  #num 表示kline本应该有多少个k线，实际操作中的确会发现有少值的情况。需要补全。
  for i in range(num):
    target_date=int(start+i*increment)
    if kline[kline_num].date == target_date:
      kline_array.append(kline[kline_num])
      kline_num+=1
    else:
      k=K()
      k.setInfo(kline.symbol,target_date,kline[kline_num-1].open,kline[kline_num-1].high,kline[kline_num-1].low,kline[kline_num-1].close,kline[kline_num-1].vol)
      k.setMarket(kline.market)
      kline_array.append(k)
      supplement_num+=1
      print('{} {} 补充日期{}'.format(k.market,k.symbol,k.formatDate()))
  kline.setInfo(kline.symbol,kline_array)
  print('{} {} 总共补充 {} 个K线'.format(kline.market,kline.symbol,supplement_num))
  return kline

def getKLines(symbol,period):
  klines=[]
  for market in markets:
    kline=market.kline(symbol,period)
    if kline.result==True:
      klines.append(kline)
    else:
      print('{} 获取K线图失败:{}'.format(symbol,kline.message))
      return []

  newklines=[]
  for kline in klines:
    newklines.append(supplementKLine(kline,period))
  
  klines=newklines

  #左边剪掉小的，右边剪掉大的
  maxStart=0
  minEnd=float("inf")
  for kline in klines:
    if kline[0].date>maxStart:
      maxStart=kline[0].date
    if kline[-1].date<minEnd:
      minEnd=kline[-1].date
  newklines=[]
  for kline in klines:
    newklines.append(kline.splitByDate(maxStart,minEnd))
  #todo 有些K线会少数据，导致切割后K线长度并不一致。记得以后修补
  return newklines

def writeFile(klines):
  with open(write_file, 'w') as f:
    f.write('{}\t{}\t{}\n'.format("date","okex","huobi","zb"))
    for i in range(len(klines[0])-2):
      f.write('{}\t{}\t{}\n'.format(klines[0][i].formatDate(),klines[0][i].close,klines[1][i].close,klines[2][i].close))
    

if __name__ == '__main__':
  
  write_file=os.path.join(os.path.dirname(__file__),"record",time.strftime('%Y-%m-%d')+'.txt')

  markets=[HuoBi('xx','xx'),Zb('xx','xx')]

  periods=['1day']

  coin_path=os.path.join(os.path.dirname(__file__),'coins.json')
  with open(coin_path,'rt') as f:
    coins=json.load(f)
  
  for period in periods:
    for symbol in coins:
      print('处理{}中...'.format(symbol))
      klines=getKLines(symbol,period)
      if len(klines) >0:
        writeFile(klines)
  print('完成')