
class Input(object):
    def __init__(self,message): 
        """Parses the IRC message into a neat input format"""
        self.raw = message
        
        split = message.split(" ")
        try:
            if split[1] == "PRIVMSG":
                self.type = "PRIVMSG"
                self.user = split[0]
                self.channel = split[2]
                self.message = message.split(" :",1)[1]
            elif split[1] == "TOPIC":
                self.type = "TOPIC"
                self.user = split[0]
                self.channel = split[2]
                self.message = message.split(" :",1)[1]
            elif split[1] == "NOTICE":
                self.type = "NOTICE"
                self.user = split[0]
                self.channel = split[2]
                self.message = message.split(" :",1)[1]
            elif split[1] == "INVITE":
                self.type = "INVITE"
                self.user = split[0]
                self.channel = message.split(" :",1)[1] #Channel invited to
                self.message = None
            elif split[1] == "QUIT":
                self.type = "QUIT"
                self.user = split[0]
                self.channel = None
                try: self.message = message.split(" :",1)[1] #Quit message
                except: self.message = ""
            elif split[0] == "PING":
                self.type = "PING"
                self.user = None
                self.channel = None
                self.message = None
            elif split[1] == "MODE":
                self.type = "MODE"
                self.user = split[0] #USER SETTING THE MODE
                self.channel = split[2]
                self.message = message.split(split[2] + " ",1)[1]
            elif split[1] == "JOIN":
                self.type = "JOIN"
                self.user = split[0] 
                self.channel = split[2]
                self.message = None
            elif split[1] == "PART":
                self.type = "PART"
                self.user = split[0]
                self.channel = split[2]
                try: self.message = message.split(" :",1)[1] #Quit message
                except: self.message = ""
            elif split[1] == "KICK":
                self.type = "KICK"
                self.user = split[0] #User kicking
                self.channel = split[2]
                self.userkicked = split[3]
                try: self.message = message.split(" :",1)[1] #Kick message
                except: self.message = ""
            else:
                self.type = split[1]
                self.channel = None
                self.message = self.raw
                self.user = None
        except:
            self.type = self.channel = self.message = self.user = None
            
    def __str__(self):
        return self.raw