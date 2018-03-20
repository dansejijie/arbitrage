# -*- coding: utf-8 -*-
import smtplib  
import email.mime.multipart  
import email.mime.text
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

    self.smtp=smtplib.SMTP()
    self.smtp.connect(self.sender_server, '25')
    self.smtp.login(self.sender, self.sender_password)
  
  def sendText(self,info,title="virtualcoin"):
    medium=Medium()
    msg = email.mime.multipart.MIMEMultipart()
    msg['Subject'] = title
    msg['From'] = self.sender  
    msg['To'] = self.recever 
    msg.attach(email.mime.text.MIMEText(info))
    print("{} {}".format(title,info))
    try:
      self.smtp.sendmail(self.sender, self.recever, msg.as_string())
      return medium
    except Exception as e:
      medium.setError(e.args[0])
      return medium

if __name__ == '__main__':
  emailSender=EmailSender()
  emailSender.sendText('哈哈哈')
  print('完成')
