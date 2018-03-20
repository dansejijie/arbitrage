# -*- coding: utf-8 -*-
import smtplib  
import email.mime.multipart  
import email.mime.text
import sys,os,requests,json
from requests.auth import HTTPBasicAuth
path=os.path.join(os.path.dirname(__file__),os.path.pardir)
sys.path.append(path)
from medium.Medium import Medium

class MessageSender(object):
  def __init__(self,username,password):    
    self.username=username
    self.password=password
  
  def sendText(self,info,mobile="13735542964",temp_id="147854"):
    medium=Medium()
    data={
    "mobile":mobile,
    "temp_id":temp_id,
    "temp_para":{
      "info":info,
      }
    };
    try:
      r=requests.post("https://api.sms.jpush.cn/v1/messages",data=json.dumps(data),headers={"Content-Type":"application/json"},auth=HTTPBasicAuth(self.username, self.password))
      r=r.json()
      if "error" in r:
        medium.setError(r.message)
      return medium
    except Exception as e:
      medium.setError(e.args[0])
      return medium

if __name__ == '__main__':
  with open(os.path.join(os.path.dirname(__file__),os.path.pardir,'config.json'),'r') as f:
    config=json.load(f)
  messageSender=MessageSender(config["message"]["username"],config["message"]["password"])
  result=messageSender.sendText('xx')
  print(result)
