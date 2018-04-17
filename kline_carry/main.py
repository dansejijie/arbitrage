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
from utils.MessageSender import MessageSender
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


  
def transBmobKline(kline):
  newKLine=[]
  for i in range(len(kline)):
    temp={}
    temp["format_date"]=time.strftime("%Y-%m-%d %H:%M", time.localtime(kline[i].date))
    temp["date"]=kline[i].date
    temp["open"]=kline[i].open
    temp["high"]=kline[i].high
    temp["low"]=kline[i].low
    temp["close"]=kline[i].close
    temp["vol"]=kline[i].vol
    newKLine.append(temp)
  return newKLine

def startHandleEvent():
  for coin in coins:
    print('开始处理{}'.format(coin))
    search_date=None
    result=bmob.queryArrayByLimit(coin,"-date",1,0)
    if len(result.extra)>0:
      search_date=result.extra[0]["date"]
    kline=market.kline(coin,"15min")
    if kline.result==True:
      start_date=kline[0].date
      end_date=kline[-1000].date
      if search_date!=None and search_date>start_date:
        start_date=search_date
      kline=getSameLine(kline,start_date,end_date)
      newLine=transBmobKline(kline)
      print('{}正在上传Bmob数据库中'.format(coin))
      result=bmob.insertArray(coin,newLine)
      if result.result==False:
        print('{}上传到Bmob数据库发生失败{}'.format(coin,result.message))
        #return error_interval_time
      else:
        with open(os.path.join(os.path.dirname(__file__),'info.txt'),"a") as f:
          f.write("{}:{} last date:{} today date:{} num:{}\n".format(time.strftime('%Y-%m-%d %H:%M:%S'),coin,search_date,start_date,len(kline)))
    else:
      print(result.message)
      ##return error_interval_time
  return correct_interval_time


#kline 可以获取2000根 因此 correct_interval_time=1080000 error_interval_time=270000 最好
if __name__ == '__main__':
  
    correct_interval_time=86400
    error_interval_time=30000
    error_num=0

    with open(os.path.join(os.path.dirname(__file__),os.path.pardir,'config.json'),'r') as f:
      config=json.load(f)
    bmob=Bmob(config["bmob"]["api_key"],config["bmob"]["secret_key"])
    market=Okex('xx','xx')
    messageSender=MessageSender(config["message"]["username"],config["message"]["password"])
    coin_path=os.path.join(os.path.dirname(__file__),'coins.json')
    with open(coin_path,'rt') as f:
      coins=json.load(f)

    try:
      while True:
        interval_time=startHandleEvent()
        if interval_time==error_interval_time:
          error_num+=1
          if error_num>12:
              error_num=0
              messageSender.sendText("错误次数太多，请尽快查看原因")
        print('程序等待下一次执行中')
        time.sleep(interval_time)
    except Exception as e:
      messageSender.sendText(e.args[0])
    print('程序退出循环')