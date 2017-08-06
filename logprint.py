import datetime

class Log(object):
    def __init__(self,debug=True): 
        self.do = debug
    
    def getTime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def time(self, msg):
        print ( "["+self.getTime()+"]" + " " + msg )
    
    def recv(self,msg):
        print ( self.getTime() + " [RECV] " + msg )
    def send(self,msg):
        print ( self.getTime() + " [SEND] " + msg )
    
    def debug(self, msg):
        if self.do:
            print ( self.getTime() + " [DEBUG] " + msg )
    def info(self, msg):
        print ( self.getTime() + " [INFO] " + msg )
    def warn(self, msg):
        print ( self.getTime() + " [WARNING] " + msg )
    def error(self, msg):
        print ( self.getTime() + " [ERROR] " + msg )
