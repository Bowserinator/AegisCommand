import socket, ssl
import socks, time, datetime

class Connection(object):
    def __init__(self,server,port,c={"nick":"AegisCommand","real_name":"Bowserinator's Bot"},SSL=True):
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if SSL: 
            self.ircsock = ssl.wrap_socket(self.ircsock)
        self.ircsock.connect((server, port)) #SSL for secure connection :D
        self.ircsock.send("USER {0} * * :".format(c["nick"]) + c["real_name"] + ".\r\n".encode('utf-8'))

    def notice(self, user, message):
        self.ircsock.send("NOTICE {} :\x01{}\x01\n".format(user, message))
    def ctcp(self, user, message):
        self.ircsock.send("PRIVMSG {} :\x01{}\x01\x01".format(user, message))
    def ping(self): 
        self.ircsock.send("PONG :pingis\n".encode('utf-8'))
    def partchan(self,chan):
        self.ircsock.send("PART {0}\n".format(chan).encode('utf-8'))
    def changenick(self,nick):
        try: self.ircsock.send("NICK {0}\n".format(nick).encode('utf-8'))
        except: pass
        
    def sendmsg(self,chan, msg):
        self.ircsock.send("PRIVMSG {0} :{1}\n".format(chan, msg))#.encode('utf-8'))
   
    def joinchan(self,chan):  
        self.ircsock.send("JOIN {0}\n".format(chan).encode('utf-8'))
    def action(self,channel,message):
        self.sendmsg(channel,"\x01ACTION " + message + "\x01")
        
    def remove(self,channel,user,message="[Default kick message]"):
        user = user.replace(" ","").replace(":","")
        self.ircsock.send("REMOVE " + channel + " " + user+ " :" + message +"\r\n")
        
    def kickuser(self,channel,user,message="[Default kick message]"):
        user = user.replace(" ","").replace(":","")
        self.ircsock.send("KICK " + channel + " " + user+ " :" + message +"\r\n")
    def opnick(self,channel,nick):
        self.ircsock.send("MODE {0} +o {1}\n".format(channel,nick).encode('utf-8'))
    def deopnick(self,channel,nick):
        self.ircsock.send("MODE {0} -o {1}\n".format(channel,nick).encode('utf-8'))
    def ban(self,channel,nick):
        self.ircsock.send("MODE {0} +b {1}\n".format(channel,nick).encode('utf-8'))
    def unban(self,channel,nick):
        self.ircsock.send("MODE {0} -b {1}\n".format(channel,nick).encode('utf-8'))
    def stab(self,channel,nick):
        self.ircsock.send("MODE {0} +q {1}\n".format(channel,nick).encode('utf-8'))
    def unstab(self,channel,nick):
        self.ircsock.send("MODE {0} -q {1}\n".format(channel,nick).encode('utf-8'))
    def unvoice(self,channel,nick):
        self.ircsock.send("MODE {0} -v {1}\n".format(channel,nick).encode('utf-8'))
    def voice(self,channel,nick):
        self.ircsock.send("MODE {0} +v {1}\n".format(channel,nick).encode('utf-8'))
    def setMode(self,channel,nick,mode):
        self.ircsock.send("MODE {0} {1} {2}\n".format(channel,mode,nick).encode('utf-8'))
        
    
    def whois(self,user):  
        self.ircsock.send("WHOIS {0}\n".format(user).encode('utf-8'))
        
    def quit(self,message="i haz quit"):
        self.ircsock.send("QUIT :{0}\n".format(message).encode('utf-8'))
    
    #Advanced functions
    def isBot(self,nick):
        #Check is a user is a bot
        data = self.gethostmask(nick)
        if data == False or data == None:
            return False
        if "bot" in data: #Checks: if a user has the word "bot" in the hostmask they're considered a bot
            return True
        if ".bc.googleusercontent.com" in data: #probably cloud9 
            return True
        if "gateway/shell/insomnia247/" in data: #Probably insomnia247 hosted bot
            return True
        return False
        
    def gethostmask(self,nick):
        self.ircsock.send("WHO {0}\r\n".format(nick).encode("UTF-8"))
        ircmsg = self.ircsock.recv(2048)
        ircmsg = ircmsg.decode("UTF-8")
        ircmsg = ircmsg.strip("\r\n")
        ircmsg = ircmsg.strip(":")
        ircmsg = ircmsg.split()
        if ircmsg[1] == "352":
            user = ircmsg[4]
            host = ircmsg[5]
            hm = "{0}!{1}@{2}".format(nick, user, host)
            return hm
        else:
            return False
            
    def getbanmask(self,nick):
        result = self.gethostmask(nick)
        if result: return "*!*@" + result.split("@")[1]
        return False
        
        