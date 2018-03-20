# -*- coding: UTF-8 -*-
import logging,logging.handlers
import os
import time
class Log:
    def getCurrentTime(self):
        return time.strftime('%Y-%m-%d')

    def createLogHandler(self):
        if self.current_time!=self.getCurrentTime():
            self.current_time=self.getCurrentTime()
            formatter=logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
            streamhandler=logging.StreamHandler()
            streamhandler.setLevel(logging.INFO)
            streamhandler.setFormatter(formatter)

            self.LOG.addHandler(streamhandler)
            filepath=os.path.join(os.path.dirname(__file__)+'/record/normal/'+self.current_time+'.log')
            filehandler=logging.FileHandler(filepath)
            filehandler.setLevel(logging.INFO)
            filehandler.setFormatter(formatter)
            self.LOG.addHandler(filehandler)
            
            filepath=os.path.join(os.path.dirname(__file__)+'/record/mark/'+self.current_time+'.log')
            filehandler=logging.FileHandler(filepath)
            filehandler.setLevel(logging.INFO)
            filehandler.setFormatter(formatter)
            self.MARK.addHandler(filehandler)

    def __init__(self):
        self.LOG=logging.getLogger('log')
        self.LOG.setLevel(logging.INFO)
        self.MARK=logging.getLogger('mark_log')
        self.MARK.setLevel(logging.INFO)
        self.current_time=''
        self.createLogHandler()

    def info(self,msg):
        self.createLogHandler()
        self.LOG.info(msg)
    def debug(self,msg):
        self.createLogHandler()
        self.LOG.debug(msg)
    def error(self,msg):
        self.createLogHandler()
        self.LOG.error(msg)
    def mark(self,msg):
        self.createLogHandler()
        self.LOG.info(msg)
        self.MARK.info(msg)

Logging =Log()
if __name__ == '__main__':
    log=Log()
    log.info('hello')
    log.mark('hi')