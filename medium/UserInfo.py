# -*- coding: UTF-8 -*-
from medium.Medium import Medium

class UserInfo(Medium):
    def __init__(self):
        Medium.__init__(self)
        self.market=None
        self.free={}
        self.freezed={}

    def __str__(self):
        if self.result:
            info="free::"
            for key,value in self.free.items():
                info+=key+":"+str(value)+" "
            info+="\n"+"freezed::"
            for key,value in self.freezed.items():
                info+=key+":"+str(value)+" "            
            return "market:{} {}".format(self.market.info)
        else:
            return 'error_message:%s' % (self.message)

    def setInfo(self, free,freezed,market=None):
        self.market=market
        self.free=free
        self.freezed=freezed

if __name__ =='__main__':
    userinfo=UserInfo()
    userinfo.setInfo({"btc":10},{"ltc":20})
    print(userinfo)
