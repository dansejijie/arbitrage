
# -*- coding: utf-8 -*-
import sys,os,requests,json,math

path=os.path.join(os.path.dirname(__file__),os.path.pardir)
sys.path.append(path)
from medium.Medium import Medium
import utils.MathHelper as MathHelper

# 最多20张表
# 最多放19个字段
# 批量插入时，每次最多50个数据
# coin 数据库
class Bmob(object):
    def __init__(self,api_key,secret_key):
        self.headers={}
        self.headers['X-Bmob-Application-Id'] = api_key
        self.headers['X-Bmob-REST-API-Key'] = secret_key
        self.headers['Content-Type'] = 'application/json'
        #批量插入最多的数量
        self.max_insert=50
        #批量查询最多的数量
        self.max_query=500
    def insert(self,table_name,data):
        medium=Medium()
        url = 'https://api.bmob.cn/1/classes/{}'.format(table_name)
        try:
            r=requests.post(url,headers = self.headers,data = json.dumps(data))
            r.encoding='utf-8'
            if r and (r.status_code==201 or r.status_code==200):
                return medium
            else:
                medium.setError(r.text)
                return medium
        except Exception as e:
            medium.setError(e.args[0])
            return medium


    """
    为了减少因为网络通讯次数太多而带来的时间浪费, 
    Bmob提供批量(batch)操作，在一个请求中对多个普通对象进行
    添加(create)、更新(update)、删除(delete) 操作，上限为50个。
    在一个批量(batch)请求中每一个操作都有自己对应的方法、路径和主体,
    这些参数可以代替你通常使用的HTTP方法. 这些操作会以发送过去的顺序来执行。
    method: POST:添加 DELETE:删除
    """
    def insertArrayByLimit(self,table_name,data):
        medium=Medium()
        if len(data)>self.max_insert:
            medium.setError('穿入数据长度不可超过50个')
            return medium

        url = 'https://api.bmob.cn/1/batch'
        newData={"requests":[]}
        for value in data:
            newData["requests"].append({
                "method":'POST',
                "path":"/1/classes/{}".format(table_name),
                "body":value,
            })
        try:
            r=requests.post(url,headers = self.headers,data = json.dumps(newData))
            r.encoding='utf-8'
            if r and (r.status_code==201 or r.status_code==200):
                return medium
            else:
                medium.setError(r.text)
                return medium
        except Exception as e:
            medium.setError(e.args[0])
            return medium

    def queryArrayByLimit(self,table_name,order='-date',limit=1,skip=0):
        medium=Medium()
        url='https://api.bmob.cn/1/classes/{}?order={}&limit={}&skip={}'.format(table_name,order,limit,skip)
        try:
            r=requests.get(url,headers = self.headers)
            r.encoding='utf-8'
            if r and (r.status_code==201 or r.status_code==200):
                newData=r.json()
                medium.extra=newData['results']
                return medium
            else:
                medium.setError(r.text)
                return medium
        except Exception as e:
            medium.setError(e.args[0])
            return medium


    def insertArray(self,table_name,data,size=50):
        medium=Medium()
        newArray=MathHelper.oneDimToMultiDim(data,size)
        for i in range(len(newArray)):
            result=self.insertArrayByLimit(table_name,newArray[i])
            if result.result==False:
                medium.setError(result.message)
                break
        return medium
    
    def queryArray(self,table_name,order='-date',limit=500):
        n=math.ceil(limit/self.max_query)
        medium=Medium()
        medium.extra=[]
        for i in range(n):
          result=self.queryArrayByLimit(table_name,order,self.max_query,i*self.max_query)
          if result.result==True:
            if len(result.extra)==0:
              break
            medium.extra=medium.extra+result.extra
          else:
            medium.setError(result.message)
            break
        if len(medium.extra)>limit:
          medium.extra=medium.extra[0:limit]
        medium.extra.reverse()
        return medium
                

if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__),os.path.pardir,'config.json'),'r') as f:
      config=json.load(f)
    bmob=Bmob(config["bmob"]["api_key"],config["bmob"]["secret_key"])
    #插入数组
    #result=bmob.insertArrayByLimit("test",[{"symbol":"eth_usdt"}])

    #result=bmob.queryArrayByLimit("test")

    #result=bmob.insert("test",{"a1":1,"a2":2,"a3":3,"a4":1,"a5":2,"a6":3,"a7":1,"a8":2,"a9":3,"a10":1,"a11":2,"a12":3,"a13":1,"a14":2,"a15":3,"a16":4,"a17":1,"a18":2,"a19":3,"a19":4})
    #test 测试插入超过限制的数组
    # L=[{'a1':1,'a2':1},{'a1':2,'a2':2},{'a1':3,'a2':3},{'a1':4,'a2':4},{'a1':5,'a2':5}]
    # result=bmob.insertArray('test',L,2)

    #test 测试批量获取数据的
    # result=bmob.queryArray("btc_usdt","-date",700)

    print(result)