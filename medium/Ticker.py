from medium.Medium import Medium
class Ticker(Medium):
    def __init__(self):
        Medium.__init__(self)
        self.market=None
        self.symbol=None
        self.last=0
        self.sell=0
        self.buy=0
        self.vol=0
    def __str__(self):
        if self.result:
            return 'market:%s symbol:%s last:%.6f sell:%.6f buy:%.6f vol:%.6f'%(self.market,self.symbol,self.last,self.sell,self.buy,self.vol)
        else:
            return 'error_message:%s'%(self.message)
    def setInfo(self,symbol,last,sell,buy,vol,market=None):
        self.market=market
        self.symbol=symbol
        self.last=last
        self.sell=sell
        self.buy=buy
        self.vol=vol

  
  