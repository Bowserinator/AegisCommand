import sys, time
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import random, commands

"""Timebomb thing"""
no_bomb_channels = ['##warriors'] #Channels where timebomb is disabled
canBombSelf = True
canBombBots = True
max_bomb_per_channel = 1
bomb_exempt = ["bowserinator"] #Users exempt

bombs = {}

def shuffle_word(word):
    word_s = word[0]
    word_e = word[-1]
    word = word[:-1][1:]
    word = list(word)
    random.shuffle(word)
    return word_s  + ''.join(word) + word_e
    
def numToWords(num,join=True):
    '''words = {} convert an integer number into words'''
    units = ['','oen','too','thre','four','five','six','seven','eigt','nine']
    teens = ['','elven','twlve','thirten','fourteen','fifteen','sixteen', \
             'seventeen','eighten','nineteen']
    tens = ['','ten','twety','thity','fory','fity','sxty','sevnty', \
            'eigty','niety']
    thousands = ['','thousd','million','billion','trillion','quadrillion', \
                 'quintillion','sextillion','septillion','octillion', \
                 'nonillion','decillion','undecillion','duodecillion', \
                 'tredecillion','quattuordecillion','sexdecillion', \
                 'septendecillion','octodecillion','novemdecillion', \
                 'vigintillion']
    words = []
    if num==0: words.append('zero')
    else:
        numStr = '%d'%num
        numStrLen = len(numStr)
        groups = (numStrLen+2)/3
        numStr = numStr.zfill(groups*3)
        for i in range(0,groups*3,3):
            h,t,u = int(numStr[i]),int(numStr[i+1]),int(numStr[i+2])
            g = groups-(i/3+1)
            if h>=1:
                words.append(units[h])
                words.append('hundred')
            if t>1:
                words.append(tens[t])
                if u>=1: words.append(units[u])
            elif t==1:
                if u>=1: words.append(teens[u])
                else: words.append(tens[t])
            else:
                if u>=1: words.append(units[u])
            if (g>=1) and ((h+t+u)>0): words.append(thousands[g]+' ')
    if join: return ' '.join(words)
    return 


class Bomb(object):
    def __init__(self, channel, target, attacker, ircsock):
        self.wires_possible = ["green", "orange", "blue", "brown", "pink", "purple", "red", "yellow"]
        self.channel = channel
        self.target = target
        self.attacker = attacker 
        self.userz = self.getNamesChannel(self.channel, ircsock.ircsock)
        
        self.detonation = random.randint(60,100)
        self.start = time.time()
        self.wires_n = random.randint(2, len(self.wires_possible))
        self.wires = []
        
        while len(self.wires) < self.wires_n:
            c = random.choice(self.wires_possible)
            if c not in self.wires:
                self.wires.append( c )
        self.selected = random.choice(self.wires)
        self.is_math = False
        
        #Math problem bomb, 15% chance
        if random.random() < 0.15:
            self.is_math = True
            rand_a = random.randint(1000,90000)
            rand_b = random.randint(1000,90000)
            
            self.selected = rand_a + rand_b
            self.selected = str(self.selected)
            
            self.attack_msg = "\x01ACTION Shoves a {} second timebomb up {}'s pants. Your only hope is to solve {} + {}: Do [cmd]cut <answer> to disarm it \x01".format(
                    self.detonation,
                    self.target,
                    numToWords(rand_a),
                    numToWords(rand_b),
                )
        else:
            self.attack_msg = "\x01ACTION Shoves a timebomb up {}'s pants. The timer is set for {} seconds. Do [cmd]cut wire to attempt to disarm it, possible wires are {}.\x01".format(
                    self.target,
                    self.detonation,
                    ", ".join(self.wires)
                )
    
    def check(self, ircsock):
        if self.channel == self.attacker:
            return "This command must be performed in a channel"
        if self.target.lower() == commands.nick.lower():
            self.target = self.attacker
            if canBombSelf:
                self.target = self.attacker
            else:
                return "You can't bomb the bot!"
        if self.target.lower() in bomb_exempt:
            return "That user is exempted!"
        if self.channel.lower() in no_bomb_channels:
            return "Timebombs are disabled for this channel."
        try:
            if len(bombs[self.channel.lower()]) > max_bomb_per_channel-1:
                return "There can only be at most {} timebombs in this channel.".format(max_bomb_per_channel)
        except Exception as e: pass
        if not canBombSelf and self.target.lower() == self.attacker.lower():
            return "You can't bomb yourself!"
        if not canBombBots and ircsock.isBot(self.target):
            return "You can't bomb bots!"
        if self.target.lower() not in self.userz:
            return "That user isn't in the channel!"
        try:
            for b in bombs[self.channel.lower()]:
                if b.target.lower() == self.target.lower():
                    return "That user already has a bomb in their pants!"
        except: pass
        return True
        
    def getNamesChannel(self, channel,irc):
        #Returns list of names in an array [["name","op"]]
        irc.send("NAMES {0}\r\n".format(channel).encode("UTF-8"))
        ircmsg = irc.recv(2048)
        ircmsg = ircmsg.decode("UTF-8")
        ircmsg = ircmsg.strip("\r\n")
        ircmsg = ircmsg.strip(":").split(" :",1)[1].split(" ")
        
        returned = []
        for i in ircmsg:
            if i.startswith("@"):
                returned.append(i.replace("@","",1).lower().encode('ascii') )
            elif i.startswith("+"):
                returned.append(i.replace("+","",1).lower().encode('ascii') )
            else:
                returned.append(i.lower().encode('ascii'))
        return returned
    
@commands.add_cmd
def bomb(args, user="",hostmask="",extra={}):
    """bomb <nick> - Timebomb someone :)
    {"category":"trivial","alias":["timebomb"]}"""
    
    args = args.split(" ")[0]
    #return "THIS IS A REMINDER TO ADD THE DETONATION TIMER FOR THE TIMEBOMB :P"
    bomb = Bomb(extra["channel"],args,user, extra["ircsock"])
    check = bomb.check(  extra["ircsock"] )
    if check != True:
        return check
    try: bombs[extra["channel"].lower()].append(bomb) 
    except: bombs[extra["channel"].lower()] = [bomb]
    
    return bomb.attack_msg.replace("[cmd]",commands.commandChar)

@commands.add_cmd
def disarm(args, user="",hostmask="",extra={}):
    """disarm <channel> - Disarm all bombs in channel
    {"category":"trivial","permLevel":50}"""
    global bombs
    if args == "":
        args = extra["channel"]
    if args == "all":
        bombs = {}
        return "All bombs disarmed :)"
    try:
        bombs[args.lower()] = []
        return "All bombs disarmed :)"
    except: 
        return "Disarm failed."

@commands.add_cmd
def bombcheat(args, user="",hostmask="",extra={}):
    """Doesn't exist as far as you're concerned
    {"category":"trivial","permLevel":1000}"""
    global bombs
    chan = extra["channel"]
    if args != "":
        chan = args
    try:
        for b in bombs[chan.lower()]:
            if b.target.lower() == user.lower():
                return b.selected
        return "Unknown bomb"
    except: 
        return "Error in cheating the bomb."
    
@commands.add_cmd
def cut(args, user="",hostmask="",extra={}):
    """cut <wire> - Cut a wire!
    {"category":"trivial","alias":["c"]}"""
    args = args.split(" ")[0]
    try:
        i = 0
        for b in bombs[extra["channel"].lower()]:
            if b.target.lower() == user.lower():
                if args.lower() in b.wires or b.is_math:
                    if args == b.selected:
                        del bombs[extra["channel"].lower()][i]
                        return "You have defused the bomb!"
                    else:
                        del bombs[extra["channel"].lower()][i]
                        extra["ircsock"].sendmsg(extra["channel"], "Wrong wire, the correct one is {}! KABOOM!".format(b.selected))
                        extra["ircsock"].kickuser( extra["channel"], user, "KABOOM")
                        return ""
                else:
                    return "You fool that wire doesn't exist! Wires are {}".format(", ".join(b.wires))
                i+= 1
        return "You can't cut the wire on someone else's bomb!"
    except: 
        return "There are no active bombs!"
        
def update_bombs(irc):
    for c in bombs:
        i = 0
        for b in bombs[c]:
            if time.time() - b.start > b.detonation:
                del bombs[c][i]
                irc.sendmsg(c, "Wrong wire, the correct one is {}! KABOOM!".format(b.selected))
                irc.kickuser( c, b.target, "KABOOM")
                return ""
            i += 1