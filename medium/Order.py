
# -*- coding: UTF-8 -*-
from medium.Medium import Medium

#status -1:已撤销  0:未成交  1:部分成交  2:完全成交 3:撤单处理中
class Order(Medium):
    def __init__(self):
        Medium.__init__(self)
        self.market=None
        self.symbol=None
        self.id=0
        self.type=None
        self.status="未成交"
        self.price=0
        self.avg_price=0
        self.amount=0
        self.deal_amount=0
    def __str__(self):
        if self.result:
            return 'market:%s symbol:%s id:%d type:%s status:%s price:%.6f avg_price:%.6f amount:%.6f deal_amount:%.6f'%(self.market,self.symbol,self.id,self.type,self.status,self.price,self.avg_price,self.amount,self.deal_amount)
        else:
            return 'error_message:%s'%(self.message)
    def setInfo(self,symbol,id,type,status,price,avg_price,amount,deal_amount,market=None):
        self.market=market
        self.symbol=symbol
        self.id=id
        self.type=type
        self.status=status
        self.price=price
        self.avg_price=avg_price
        self.amount=amount
        self.deal_amount=deal_amount

    def setOrder(self,order):
        self.market=order.market
        self.symbol=order.symbol
        self.id=order.id
        self.type=order.type
        self.status=order.status
        self.price=order.price
        self.avg_price=order.avg_price
        self.amount=order.amount
        self.deal_amount=order.deal_amount
