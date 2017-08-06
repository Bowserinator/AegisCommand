import sys, wolfram, re, requests, math, socket, general
from decimal import Decimal
import wikipedia
import web as web2
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
    
import commands, time, random

facts = open('General/facts.txt','r').readlines()
web = web2.Web()

#Some general commands

@commands.add_cmd
def wiki(args,user="",hostmask="",extra={}):
    """wiki <query> - Query wikipedia
    {"category":"general"}"""
    try: return "\x01Results: \x0f" + wikipedia.summary(args, sentences=3).encode('ascii','ignore').decode('ascii').strip() 
    except: return "\x01[Error]\x0f No page found!"
    
@commands.add_cmd
def wolf(args,user="",hostmask="",extra={}):
    """wolf <query> - Query WolframAlpha, great for calculations or facts.
    {"category":"general"}"""
    result = wolfram.wolfram(args)
    if not result:
        return "There were no results for that query."
    return "\x02Result: \x0f" + " \x02|\x0f ".join(result[0]["raw"])[:320]
    
@commands.add_cmd
def help(args,user="",hostmask="",extra={}):
    """help [command] - Get help for a command
    {"category":"general"}"""
    args = args.lstrip().rstrip().lower()
    if args == "":
        args = "help"
    if args == "me":
        return "Attempting to call ambulance... [SEGFAULT]"
    for c in commands.commands:
        if c.name.lower() == args and c.exist:
            return "\x02Help: \x0f" + c.helpText
    return "Command '{}' not found".format(args)


@commands.add_cmd
def list(args,user="",hostmask="",extra={}):
    """list [category] - List all the commands.
    {"category":"general"}"""
    args = args.lstrip().rstrip().lower()
    if args == "":
        categories = []
        for c in commands.commands:
            if c.catagory not in categories:
                categories.append(c.catagory)
        return "\x02Do " + commands.commandChar + "list [Category]: \x0f" + ", ".join(categories)
    else:
        total = []
        for c in commands.commands:
            if c.catagory == args and c.show and c.exist:
                total.append( c.name )
        if len(total) == 0:
            return "Invalid list category!"
        return "\x02Commands: \x0f" + ", ".join(total)
        
        
@commands.add_cmd
def fact(args,user="",hostmask="",extra={}):
    """fact [search start] - Get a random fact
    {"category":"general"}"""
    args = args.lower()
    if args.lstrip().rstrip() != "":
        found = []
        for i in facts:
            if args in i.lower():
                found.append( i )
        if len(found) > 0:
            return random.choice(found)
        return "No fact found that contains that query."
    return random.choice(facts)
    
@commands.add_cmd
def isBot(args,user="",hostmask="",extra={}):
    """isBot - Check if a user is a bot.
    {"category":"general"}"""
    try: return "The user {} is probably {}a bot.".format(args, {True:"",False:"not "}[extra["ircsock"].isBot(args.lower())] )
    except: return "Could not get data for that user."
    
    
@commands.add_cmd
def eval_irc(args,user="",hostmask="",extra={}):
    """eval - Evaluate some code
    {"category":"config","permLevel":100,"name":"eval"}"""
    ircsock = extra["ircsock"]
    channel = extra["channel"]
    
    iovoid  = Iovoid()
    nazi    = "NAZI"
    defined = True
    undefined = False
    
    try:
        return str(eval(args)) or "[No output]"
    except Exception as e:
        return "\x02[Error]\x0f: " + str(e)
    
@commands.add_cmd
def ping(args,user="",hostmask="",extra={}):
    """ping - Checks if the bot is alive
    {"category":"general"}"""
    return "PONG! PONG! PONG!"
    
@commands.add_cmd
def pong(args,user="",hostmask="",extra={}):
    """pong - It's ping you moron.
    {"category":"general","show":false}"""
    return "It's ping you moron"
    
@commands.add_cmd
def ding(args,user="",hostmask="",extra={}):
    """ding - DING DONG!
    {"category":"general","show":false}"""
    return "DING DONG DING"
    
@commands.add_cmd
def dong(args,user="",hostmask="",extra={}):
    """dong - It's ding you moron.
    {"category":"general","show":false}"""
    return "It's ding you moron"

@commands.add_cmd
def status(args,user="",hostmask="",extra={}):
    """status - Get some bot stats.
    {"category":"config","threaded":false}"""
    return "I started running at " + str(commands.start_time[0]).split(".")[0] + " and have been up for " + str(humanize_time( int(time.time() - commands.start_time[1]) ,"seconds")) + "."

INTERVALS = [1, 60, 3600, 86400, 604800, 2419200, 29030400]
NAMES = [('second', 'seconds'),
         ('minute', 'minutes'),
         ('hour', 'hours'),
         ('day', 'days'),
         ('week', 'weeks'),
         ('month', 'months'),
         ('year', 'years')]

def humanize_time(amount, units):
    result = []
    unit = ['seconds', 'minutes', 'hours', 'days', 'weeks', 'months', 'years'].index(units)
    amount = amount * INTERVALS[unit]
    
    for i in range(len(NAMES)-1, -1, -1):
        a = amount / INTERVALS[i]
        if a > 0:
            result.append( (a, NAMES[i][1 % a]) )
            amount -= a * INTERVALS[i]
    returned = ""
    for i in result:
        returned += str(i[0]) + " " + i[1] + " "
    return returned.lstrip().rstrip() 
    
class Iovoid(object): # Haha very funny.
    def __init__(self):
        self.grade = "A"
        self.real_grade = "F"
        
    def isNazi(self):
        return True
    
    def __eq__(self, other):
        if other == "NAZI":
            return True
        return False
        


#GEOIP-------------------------
def DMS(degree):
    #Returns DMS for degree
    degree = Decimal(degree)
    d = Decimal(math.floor(degree))
    m = (degree - d)*Decimal("60")
    m = Decimal(math.floor(m))
    s = (degree - d - m/Decimal("60"))*Decimal('3600')
    return d,m,s


# def geoip(args,user="",hostmask="",extra={}):
#     #GEOIP <USER>
#     #Replace with http://ipinfo.io/ ?
    
#     if len(re.findall('[a-zA-Z]+',args)) > 0:
#         args = socket.gethostbyname(args)
            
#     match = geolite2.lookup(args)
#     if match == None: return "Could not geoip the given ip address."
    
#     coords = match.location
#     c1 = DMS(coords[0]); c2 = DMS(coords[1])
#     googleUrl = "https://www.google.com/maps/place/{}%20{}'{}%22N+{}%20{}'{}%22E".format(c1[0],c1[1],round(c1[2],3),c2[0],c2[1],round(c2[2],3))
#     if c1[0] < 0: googleUrl = "https://www.google.com/maps/place/{}%20{}'{}%22S+{}%20{}'{}%22E".format(abs(c1[0]),c1[1],round(c1[2],3),c2[0],c2[1],round(c2[2],3))
#     if c2[0] < 0: googleUrl = googleUrl.replace("+-","+").replace("E","W")
#     googleUrl = web.isgd(googleUrl)
    
#     return "\x02Ip: \x0f{} | \x02Subdivision: \x0f{} | \x02Country: \x0f{} | \x02Continent: \x0f{} | \x02Map: \x0f {} | \x02Location: \x0f {} | \x02Time Zone: \x0f {}".format(
#         match.ip,
#         str(match.subdivisions).replace("frozenset([","").replace("])",""),
#         match.country,
#         match.continent,
#         googleUrl,
#         match.location,
#         match.timezone
#     )

@commands.add_cmd
def geoip(args,user="",hostmask="",extra={}):
    """geoip <ip> - Get geoip info
    {"category":"general","threaded":false}"""
    result = extra["ircsock"].gethostmask(args)
    isUser = False
    if result:
        try: args = result.split("@")[1].split("gateway")[1].replace("ip","").replace("/","")
        except: args = result.split("@")[1]
        isUser = True
    
    args = args.replace("https://","").replace("http://","").replace("www.","")
    
    try:
        if len(re.findall('[a-zA-Z]+',args)) > 0:
            try: args = socket.gethostbyname(args)
            except: pass
        response = requests.get("http://ipinfo.io/"+args)
        info = response.json()
    
        coords = info["loc"].split(",")
        c1 = DMS(coords[0]); c2 = DMS(coords[1])
        googleUrl = "https://www.google.com/maps/place/{}%20{}'{}%22N+{}%20{}'{}%22E".format(c1[0],c1[1],round(c1[2],3),c2[0],c2[1],round(c2[2],3))
        if c1[0] < 0: googleUrl = "https://www.google.com/maps/place/{}%20{}'{}%22S+{}%20{}'{}%22E".format(abs(c1[0]),c1[1],round(c1[2],3),c2[0],c2[1],round(c2[2],3))
        if c2[0] < 0: googleUrl = googleUrl.replace("+-","+").replace("E","W")
        try: googleUrl = web.tinyurl(googleUrl)
        except: 
            try: googleUrl = web.isgd(googleUrl)
            except: pass
        
        returned = "\x02Location: \x0f{}, {}, {} {} | \x02Hostname: \x0f{} ({}) | \x02Provider: \x0f{} | \x02Maps: \x0f{} ({})".format(
            info.get("city") or "[Unknown]",
            info.get("region") or "[Unknown]",
            info.get("country") or "[Unknown]",
            info.get("postal") or "[Unknown]",
            
            info.get("hostname") or "[Unknown]",
            info.get("ip") or "[Unknown]",
            info.get("org") or "[Unknown]",
            googleUrl,
            info.get("loc") or "[Unknown]"
        )
        return returned
    except Exception as e:
        if isUser: 
            return "Hostmask found or could not get ip address info."
        return "Geoip error: {}".format(e)
        
@commands.add_cmd
def modeReference(args,user="",hostmask="",extra={}):
    """modeReference <mode> - Get help for a mode
    {"category":"general"}"""
    return modeReference2(args)

def modeReference2(mode):
    returned = "\x02User Modes: \x0f"
    
    if mode == "D":
        returned = returned + "This prevents you from receiving channel messages. You will probably not want to set this in most cases. (It is used by services.)"
    elif mode == "g":
        returned = returned + "You can set this umode to prevent you from receiving private messages from anyone not on a session-defined whitelist. "
    elif mode == "i":
        returned = returned + "This prevents you from appearing in global WHO/WHOIS by normal users, and hides which channels you are on."
    elif mode == "q":
        returned = returned + "This user mode prevents you from being forwarded to another channel because of channel mode +f (see below) or by a ban (see +b below). Instead of being forwarded to another channel, you'll be given a message as to why you could not join."
    elif mode == "R":
        returned = returned + "This user mode prevents users who are not identified to NickServ from sending you private messages."
    elif mode == "w":
        returned = returned + "This user mode lets you see the wallops announcement system. Important network messages will be sent out via global notices; this is only for non-critical announcements and comments which may be of interest."
    elif mode == "z":
        returned = returned + "You will have this user mode if you connect to freenode with SSL"
        
    returned = returned + " \x02Channel Modes: \x0f"
    if mode == "b":
        returned = returned + "Bans user. /mode #channel +b lists bans. Extbans: /ban $a:account - Bans all accounts identified to account. /ban $j:channel - Bans all users banned in channel from current channel. $r - Bans realname. $x - String parm against full name. $z - bans all SSL. /mode #channel +b [banmask]$#redirectchannel"
    elif mode == "c":
        returned = returned + "Filters out formatting such as color and bold words."
    elif mode == "e":
        returned = returned + "Exempts person from bans, overrides +q and +b bans"
    elif mode == "f":
        returned = returned + "/mode #channel1 +if #channel2 Forwards user to channel2 if not invited"
    elif mode == "F":
        returned = returned + "This mode can be set by any channel operator to allow operators in other channels to set bans to forward clients to their channel, without requiring ops in it."
    elif mode == "g":
        returned = returned + "Allow anyone to invite."
    elif mode == "i":
        returned = returned + "Makes the channel invite only."
    elif mode == "I":
        returned = returned + "Exempts client (Same format as bans) from having to be invited to join."
    elif mode == "j":
        returned = returned + "/mode #channel n:t  Only allows n users to join every t seconds. Invited users can join regardless of this, but are still counted."
    elif mode == "k":
        returned = returned + "Sets a password to join the channel, to join type /join #channel <password>"
    elif mode == "l":
        returned = returned + "Sets limit to how many users can join channel."
    elif mode == "L":
        returned = returned + "Set only by freenode staff, allows a channel to have longer than normal ban, exempt, and invite exemption lists."
    elif mode == "m":
        returned = returned + "When a channel is set +m, only users who are opped or voiced on the channel can send to it. This mode does not prevent users without voice or op from changing nicks."
    elif mode == "n":
        returned = returned + "Users outside the channel may not send messages to it."
    elif mode == "p":
        returned = returned + "When set, the KNOCK command cannot be used on the channel to request an invite, and users will not be shown the channel in whois replies unless they are on it. Unlike on some ircds, +p and +s can be set together."
    elif mode == "P":
        returned = returned + "Only set by freenode staff, makes the channel stay even if there are no users in it."
    elif mode == "q":
        returned = returned + "This mode prevents users who are not identified to NickServ from joining the channel. Users will receive a server notice explaining this if they try to join. /mode #channel +q $~a can be used to prevent unregistered users from speaking in channel while allowing them to join."
    elif mode == "Q":
        returned = returned + "Users will not be able to be forwarded (see +f above) to a channel with +Q."
    elif mode == "r":
        returned = returned + "This mode prevents users who are not identified to NickServ from joining the channel. "
    elif mode == "s":
        returned = returned + "Only users connected via SSL may join the channel while this mode is set. Users already in the channel are not affected. "
    elif mode == "t":
        returned = returned + "When +t is set, only channel operators may modify the topic of the channel. This mode is recommended in larger, more public channels to protect the integrity of the topic."
    elif mode == "z":
        returned = returned + "When +z is set, the effects of +b, +q, and +m are relaxed. For each message, if that message would normally be blocked by one of these modes, it is instead sent to all the users who are currently set +o (channel operator). This is intended for use in moderated debates."
    return returned

@commands.add_cmd
def define(args,user="",hostmask="",extra={}):
    """define <word> [definition number] - Return definition for a word.
    {"category":"general","alias":["def"]}"""
    if extra["channel"] == "##powder-mc": return "Disabled for this channel."
    #Define word <definition>
    number = args.split(" ")[-1]
    try: float(number); n = int(float(number))
    except: n = None
    
    defi = general.define(args.replace(str(n),""))
    if n and n >= 0 and n < len(defi): return "\x02Def: \x0f" + defi[n].encode('utf8')
    
    if len(defi) == 0: return "Word not found."
    if len(defi) > 1 and len(defi[0]) < 270: return "\x02Def: \x0f" + defi[0].encode('utf8') + "; " + defi[1].encode('utf8')
    return "\x02Def: \x0f" + defi[0].encode('utf8')

@commands.add_cmd
def translate(args,user="",hostmask="",extra={}):
    """translate <phrase> to_lan=[lan code] from_lan=[lan code] - Translate a pharse.
    {"category":"general"}"""
    #Translate phrase to_lan=<> from_lan=<>
    args = args+" "
    lan = args.split(" ")
    to_lan = "auto"; from_lan = "auto"
    for i in lan:
        if i.startswith("to_lan="):
            to_lan = i.split("=")[1]
        elif i.startswith("from_lan="):
            from_lan = i.split("=")[1]
    args = args.replace("from_lan="+from_lan,"")
    args = args.replace("to_lan="+to_lan,"")
    return general.translate(args, to_lan, from_lan)

@commands.add_cmd
def attack(args,user="",hostmask="",extra={}):
    """attack <user> - Attack a user
    {"category":"general"}"""
    args = args.lstrip().rstrip()
    attacks = [
        "drops a cool black planet on {}",
        "eats {} for breakfast.",
        "tackles {} and annihilates {} completely, ending {}'s thoughts of revenge. ",
        "smashes {}'s face through 4 layers of glass.",
        "whacks {} into space.",
        "breathes out a stream of white hot fire, melting {}'s face instantly.",
        "takes out a sharpness V sword and slices {} in half.",
        "detonates an antimatter missile onto {}.",
        "fires the B.E. Space Laser, shooting a beam of death towards {}.",
        "takes the brush and drops some SING near where {} was standing.",
        "borrows a banhammer and smashes it on {}'s skull.",
        "beats {} in a game of chess, causing {} to die of shame.",
        "forces {} to listen to Justin Bieber, causing their eardrums to explode.",
        "shoves {} into a vat of sodium hydroxide.",
        "types /kill @p[Name={}]",
        "types !set type {} none in the console.",
        "straps {} onto a rocket heading towards the sun.",
        "drops an anvil onto {}, cracking their skull",
    ]
    
    return "\x01ACTION "+random.choice(attacks).replace("{}",args)+ "\x01"