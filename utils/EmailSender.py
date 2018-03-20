# -*- coding: utf-8 -*-
import smtplib  
from email.mime.text import MIMEText
import sys,os,requests,json
path=os.path.join(os.path.dirname(__file__),os.path.pardir)
sys.path.append(path)
from medium.Medium import Medium

class EmailSender(object):
  def __init__(self,sender_server,sender_username,sender_password):
    
    self.sender_server=sender_server
    self.sender=sender_username
    self.sender_password=sender_password
    self.recever="dansejijie@yeah.net"

    

    
  
  def sendText(self,info,title="virtualcoin"):
    medium=Medium()

    msg = MIMEText(info,_subtype='plain')
    msg['Subject'] = title
    msg['From'] = self.sender  
    msg['To'] = self.recever 
  
    try:
      self.smtp=smtplib.SMTP()
      self.smtp.connect(self.sender_server, '25')
      self.smtp.login(self.sender, self.sender_password)
      self.smtp.sendmail(self.sender, self.recever, msg.as_string())
      self.smtp.close()
      return medium
    except Exception as e:
      medium.setError(e.args[0])
      return medium

if __name__ == '__main__':
  with open(os.path.join(os.path.dirname(__file__),os.path.pardir,'config.json'),'r') as f:
      config=json.load(f)
  emailSender=EmailSender(config["email"]["126"]["server"],config["email"]["126"]["username"],config["email"]["126"]["password"])
  emailSender.sendText('哈哈哈切')
  print('完成')
