#SAVE DATA FOR STUFF HERE
import connection, logprint, traceback
import random, json, time, datetime, threading

log = logprint.Log()
ircsock = connection.Connection("irc.freenode.net",6697)
commands = []
start_time = [datetime.datetime.now(), time.time()]

userPerms = {
    "unaffiliated/bowserinator":10000,
}

#Stuff loaded from JSON
channels = ["##bowserinator"]
nick = "AegisCommand"
nick2 = "AegisCommand"+ str(random.randint(0,1000))
commandChar = "@"


enablePM = True
unsafeCommandChar = False
quizSolve = False
blacklistchan = ["#powder","#freenode"]
password = "password_here"


#COMMAND DECORATOR
#=====================================================#
class Command(object):
    def __init__(self,name,helpText,catagory,permLevel,commandChar,autoHelp=True,chanRestrictions={},show=True, threaded=True, alias = [], exist=True): #Channels/PM restrictions
    #Catagory is for help, ie calc or general
        self.chanRestrictions = chanRestrictions
        self.catagory = catagory
        self.name = name
        self.show = show
        self.helpText = helpText
        self.permLevel = permLevel
        self.commandChar = commandChar
        self.function = None
        self.autoHelp = autoHelp
        self.threaded = threaded
        self.alias = alias
        self.exist = exist
        
    def __str__(self):
        return self.name
        
def add_cmd( func ):
    stuff = json.loads(func.__doc__.split("\n")[1])
    thing = {}
    thing["name"] = stuff.get("name") or func.__name__
    thing["helpText"] = stuff.get("helpText") or "Default help text"
    thing["category"] = stuff.get("category") or "Unknown"
    thing["cmdChr"]   = stuff.get("cmdChr") or commandChar
    thing["permLevel"]= stuff.get("permLevel") or 0
    thing["autoHelp"] = stuff.get("autoHelp") or True
    try: 
        thing["show"]     = stuff["show"]
    except: thing["show"] = True
    
    try: 
        thing["exist"]     = stuff["exist"]
    except: thing["exist"] = True
    thing["threaded"] = stuff.get("threaded") or True
    thing["alias"] = stuff.get("alias") or []
    stuff = thing
    c = Command( (stuff["name"] or func.__name__), func.__doc__.split("\n")[0], stuff["category"], stuff["permLevel"], stuff["cmdChr"], stuff["autoHelp"], {}, stuff["show"], stuff["threaded"], stuff["alias"], stuff["exist"]) 
    c.function = func
    commands.append(c)
    return func
    
def runCommand(args, hostmask, user, extra, command, q, channel):
    hostmask, user = user, hostmask
    try:
        returned = command.function( args, hostmask, user, extra )
    except Exception as e: 
        traceback.print_exc()
        if command.autoHelp: returned = command.helpText
    q.put( [channel,returned] )
    return ""

def getCommandByName( name ):
    for i in commands:
        if name == i.name:
            return i
    return False
    

    
#IMPORT EVERYTHING
import Bowserbucks, General, Trival, config, Timebomb, calc, Reminders, MC

def r(): #Multithreaded reload :)
    commands = []
    for x in [Bowserbucks, General, Trival, config, Timebomb, calc, Reminders, MC]: #MC
        t1 = threading.Thread(target=reload, args=(x,))
        t1.setDaemon(True); 
        t1.start();
        

def update_bombs(irc):
    Timebomb.update_bombs(irc)
def update_reminders(user,channel,message,irc):
    Reminders.update_reminders(user,channel,message,irc)
    
