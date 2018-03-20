import time
from medium.Medium import Medium

class KLine(Medium):
    def __init__(self):
        Medium.__init__(self)
        self.kline=[]
        self.symbol=None
        self.market=None
    def __len__(self):
        return len(self.kline)
    def __getitem__(self,key):
        return self.kline[key]
    def __setitem__(self,key,value):
        self.kline[key]=value
    def __str__(self):
        if self.result:
            return 'market:%s symbol:%s length:%d'%(self.market,self.symbol,len(self.kline))
        else:
            return 'error_message:%s'%(self.message)
    def setInfo(self,symbol,kline,market=None):
        self.symbol=symbol
        self.kline=kline
        self.market=market

    def setMarket(self,market):
        self.market=market

    def split(self,start,end):
        kline_array=self.kline[start:end]
        kline=KLine()
        kline.setInfo(self.symbol,kline_array)
        return kline
    
    def splitByDate(self,date1,date2):
        start=0
        end=0
        for k in self.kline:
          if k.date < date1:
            start+=1
          if k.date<date2:
            end+=1
        kline_array=self.kline[start:end+1]
        kline=KLine()
        kline.setInfo(self.symbol,kline_array)
        return kline

    def formatObjectArray(self):
        new_array=[]
        for k in self.kline:
            new_array.append(k.formatObject())
        return new_array