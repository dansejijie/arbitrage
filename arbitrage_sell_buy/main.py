# -*- coding: utf-8 -*-
import sys,os,time,json
sys.path.append(os.path.join(os.path.dirname(__file__),os.path.pardir))

from medium.Medium import Medium
from medium.Ticker import Ticker
from medium.Order import Order
from market.Okex import Okex

from bmob.Bmob import Bmob
#from utils.EmailSender import EmailSender
from utils.MessageSender import MessageSender



def updateDepth():
    print('开始更新价格中')
    medium=Medium()
    depth=market.depth(data["symbol"])
    if depth.result:
        data["buy1"]=depth.bids[0][0]
        data["buy2"]=depth.bids[1][0]
        data["buy3"]=depth.bids[2][0]
        print("最新价格 buy1:{} buy2:{} buy3:{}".format(data["buy1"],data["buy2"],data["buy3"]))
    else:
        data["error_flag"]+=1
        medium.setError(depth.message)
    return medium

def updateOrder():
    print('开始更新订单状态')
    medium=Medium()
    for i in range(len(data["orders"])):
        order=data["orders"][i]
        if order.status!="完全成交" and order.status!="已撤销":
            newOrders=market.order(data["symbol"],order.id)
            if newOrders[0].result:
                order.setOrder(newOrders[0])
            else:
                data["error_flag"]+=1
                medium.setError(newOrders[0].message)
                break
    return medium

def findOuterPriceOrder():
    print('开始寻找过价订单')
    medium=Medium()
    for i in range(len(data["orders"])):
        order=data["orders"][i]
        if order.status=="部分成交" or order.status=="未成交":
            if order.price>data['buy2'] or order.price<data['buy3']:
                current_time=time.time()
                if current_time-order.date<2800:
                    continue
                newOrder=market.cancelOrder(order.symbol,order.id)
                if newOrder.result:
                    if order.status=="未成交":
                        order.status="已撤销"
                        print('market:{} symbol:{} 因越价已撤销'.format(order.market,order.symbol))
                    else:
                        if order.deal_amount<order.amount*(1-0.9):
                            order.status="已撤销"
                            print('market:{} symbol:{} 因越价已撤销'.format(order.market,order.symbol))
                        else:
                            order.status="完全成交"
                            print('market:{} symbol:{} 因越价但成交部分因此改为全部成交'.format(order.market,order.symbol))
                else:
                    data["error_flag"]+=1
                    medium.setError(newOrder.message)
    return medium

def findMissOrder():
    print('开始寻找未挂订单')
    medium=Medium()
    for i in range(len(data["sell_buy"])):
        target_buy=data["sell_buy"][i]
        if target_buy in data:
            flag=False
            for j in range(len(data["orders"])):
                if data[target_buy]==data["orders"][j].price:
                    flag=True
                    break
            if flag==False:
                price=data[target_buy]
                amount=(data["{}_assets".format(target_buy)]*1.0)/price
                order=market.trade(data["symbol"],price,amount,"buy")
                order.date=time.time()
                if order.result:
                    data["orders"].append(order)
                    print("弥补缺失订单 market:{} symbol:{} price:{} amount:{}".format(data["market"],data["symbol"],order.price,order.amount))
                else:
                    data["error_flag"]+=1
                    medium.setError(order.message)
                    break
    return medium

def handleOrderStatus():
    print("开始处理订单状态")
    i=0
    while i<len(data["orders"]):
        order=data["orders"][i]
        if order.status=="完全成交":
            info={
                "market":data["market"],
                "symbol":data["symbol"],
                "id":order.id,
                "type":order.type,
                "avg_price":order.avg_price,
                "deal_amount":order.deal_amount
            }
            bmob.insert("trade",info)
            #emailSenderemailSender.sendText(json.dumps(info))
            messageSender.sendText(json.dumps(info))
            data["finish_order_num"]+=1
            del data["orders"][i]
        elif order.status=="已撤销":
            print("market:{} symbol:{} 订单已被撤销".format(data["market"],data["symbol"]))
            del data["orders"][i]
        else:
            i+=1
    print("当前持有订单数:{} 已完成订单数:{}".format(len(data["orders"]),data["finish_order_num"]))

def finish():
    print("{} {} {}开始结算".format(time.strftime('%Y-%m-%d %H:%M:%S'),data["market"],data["symbol"]))
    diff_time=time.time()-data["error_target_time"]
    if data["error_flag"]<5 and diff_time >10*60:
        data["error_flag"]=0
        data["error_target_time"]=time.time()
    elif data["error_flag"]>=5:
        data["error_flag"]=0
        data["error_target_time"]=time.time()
        print("当前时间:{} 需等待时间:1小时".format(time.strftime('%Y-%m-%d')))
        print("发生错误太多，暂停运行")

        return 60*60
    return data["interval_time"]
            

def run():
    while True:
        result=updateDepth()
        if result.result==False:
            print(result.message)
            interval_time=finish()
            time.sleep(interval_time)
            continue

        result=updateOrder()
        if result.result==False:
            print(result.message)
            interval_time=finish()
            time.sleep(interval_time)
            continue

        result=findOuterPriceOrder()
        if result.result==False:
            print(result.message)
            interval_time=finish()
            time.sleep(interval_time)
            continue
        
        result=findMissOrder()
        if result.result==False:
            print(result.message)
            interval_time=finish()
            time.sleep(interval_time)
            continue

        handleOrderStatus()

        interval_time=finish()
        time.sleep(interval_time)
    
    

if __name__ == "__main__":
    symbol="cag_usdt"
    if len(sys.argv)==1:
        env="beta"
    else:
        env="release"
        symbol=sys.argv[1]
    
    with open(os.path.join(os.path.dirname(__file__),'config/okex/{}.json'.format(symbol)),'r') as f:
        data=json.load(f)

    data["market"]="okex"
    data["symbol"]=symbol
    data["orders"]=[]
    data["error_target_time"]=time.time()
    data["finish_order_num"]=0
    
    with open(os.path.join(os.path.dirname(__file__),os.path.pardir,'config.json'),'r') as f:
        config=json.load(f)
    bmob=Bmob(config["bmob"]["api_key"],config["bmob"]["secret_key"])
    market=Okex(config[env]["okex"]["api_key"],config[env]["okex"]["secret_key"])
    #emailSender=EmailSender(config["email"]["126"]["server"],config["email"]["126"]["username"],config["email"]["126"]["password"])
    messageSender=MessageSender(config["message"]["username"],config["message"]["password"])
    if env!="release":
        messageSender.setDebug(True)
    try:
        run()
    except Exception as e:
        messageSender.sendText("{} {} 发生异常错误:{}".format(data["market"],data["symbol"],e.args[0]))
    #emailSender.sendText("程序未知原因退出",title="{} {}".format(data["market"],data["symbol"]))