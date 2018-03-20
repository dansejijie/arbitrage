class MarketClient:
  
  def __init__(self,api_key,secret_key):
    self.api_key=api_key
    self.secret_key=secret_key
  
  def ticker(self,symbol):
    pass
  def userinfo(self):
    pass
  def order(self,order_id,symbol):
    pass
  def cancelOrder(self,order_id,symbol):
    pass
  def trade(self,amount,price,symbol,type):
    pass
  def depth(self,symbol,size=1):
    pass
  
  