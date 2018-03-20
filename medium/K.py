import time
from medium.Medium import Medium

class K(Medium):
    def __init__(self):
        Medium.__init__(self)
        self.symbol=None
        self.date=None
        self.open=0
        self.high=0
        self.low=0
        self.close=0
        self.vol=0
        self.market=None
    def __str__(self):
        if self.result:
            #转换成localtime
            time_local = time.localtime(self.date)
            #转换成新的时间格式(2016-05-05 20:28:54)
            dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            return 'market:%s symbol:%s date:%s open:%s high:%s low:%s close:%s vol:%s'%(self.market,self.symbol,dt,self.open,self.high,self.low,self.close,self.vol)
        else:
            return 'error_message:%s'%(self.message)
    def setInfo(self,symbol,date,open,high,low,close,vol,market=None):
        self.symbol=symbol
        self.date=date
        self.open=open
        self.high=high
        self.low=low
        self.close=close
        self.vol=vol
        self.market=market
    
    def setMarket(self,market):
        self.market=market
    
    def formatDate(self):
        time_local = time.localtime(self.date)
        #转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d:%H:%M:%S",time_local)
        return dt
    
    def formatObject(self):
        temp={
            "date":self.date,
            "open":self.open,
            "high":self.high,
            "low":self.low,
            "close":self.close,
            "vol":self.vol,
        }
        return temp
