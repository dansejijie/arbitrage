# -*- coding: utf-8 -*-
class Medium:
    def __init__(self):
        self.result=True
        self.message='ok'
        #用来额外捎带数据的
        self.extra=''
    def __str__(self):
        return self.message
    def setError(self,message="error"):
        self.result=False
        self.message=message
    def getResult(self):
        return self.result
    def getMessage(self):
        return self.message
    def setResult(self,result):
        self.result=result
    def setMessage(self,message):
        self.message=message