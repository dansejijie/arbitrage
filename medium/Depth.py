from medium.Medium import Medium
class Depth(Medium):
    def __init__(self):
        Medium.__init__(self)
        self.market=None
        self.symbol=None
        self.asks=[]
        self.bids=[]
    def __str__(self):
        if self.result:
            return 'market:%s symbol:%s asks size:%d bids size:%d'%(self.market,self.symbol,len(self.asks),len(self.bids))
        else:
            return 'error_message:%s'%(self.message)
    def setInfo(self,symbol,asks,bids,market=None):
        self.market=market
        self.symbol=symbol
        self.asks=asks
        self.bids=bids
