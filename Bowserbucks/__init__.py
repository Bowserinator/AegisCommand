import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
    
import commands
import json

SAVE_TIMEOUT = 30 #Save every this many seconds

#Open the datafile
data = open('Bowserbucks/capitalism.json', 'r').read()
if data == "": data = {}
else: data = json.loads(data)


#SOME FUNctions :)
#===================================
def monify(string):
    return u"\u0243".encode("utf8") + "{:,}".format(string)
    
def getHostData(host, data):
    host = host.lower().lstrip().rstrip()
    for key in data:
        if key == host: return data[key]
    return None
    
def guessHost(nick, data): #Guess hostmask based on nick
    nick = nick.lower().lstrip().rstrip()
    for key in data:
        if nick in key:
            return key
    return None

#===================================
#Make the item list
class Item(object):
    def __init__(self, name, cost, description, category, show=True, useable=True, buyable=True):
        self.name = name
        self.cost = cost
        self.desc = description
        self.show = show
        self.category = category
        self.buyable = buyable
        self.useable = useable
    
items = {
    "thing":Item("Thing", 1, "A thingy that does things. Looks like you've been scammed.", "other"),
}

@commands.add_cmd
def buy(args,user="",hostmask="",extra={}):
    """buy <item> - Buy an item from the shop.
    {"category":"bowserbucks"}"""
    args = args.lstrip().rstrip()
    return doCapitalism( args, user, hostmask, extra, "BUY" )


#CASH COMMANDS
@commands.add_cmd
def bal(args,user="",hostmask="",extra={}):
    """bal [user] - Get balance in account.
    {"category":"bowserbucks","autoHelp":false}"""
    args = args.lstrip().rstrip()
    return doCapitalism( args, user, hostmask, extra, "BAL" )
    
@commands.add_cmd
def cash(args,user="",hostmask="",extra={}):
    """cash [user] - Get balance in account.
    {"category":"bowserbucks","autoHelp":false}"""
    args = args.lstrip().rstrip()
    return doCapitalism( args, user, hostmask, extra, "BAL" )

#STORE COMMANDS
@commands.add_cmd
def store(args,user="",hostmask="",extra={}):
    """store [list] - Check the BowserBucks store.
    {"category":"bowserbucks","autoHelp":false}"""
    args = args.lstrip().rstrip()
    return doCapitalism( args, user, hostmask, extra, "STORE" )





"""All the actual capitalism commands
Decided to put them all into one function to save space"""

def doCapitalism( args, user, hostmask, extra, t ):
    #Load the database
    data = open('Bowserbucks/capitalism.json', 'r').read()
    if data == "": data = {}
    else: data = json.loads(data)
    
    returned = ""
    #BALANCE COMMAND
    #============================================================================================================
    if t == "BAL": 
        thing = getHostData(hostmask, data)
        if thing == None: #Account doesn't exisit yet
            data[hostmask.lower()] = [ 1000, {} ] #Balance, items
            returned = "\x02[SUCCESS]\x0f Account successfully added for this hostmask!"
        else:
            if args == "": returned = "\x02Balance: \x0f{}".format(monify(data[hostmask.lower()][0]))
            else:
                try: returned  = "\x02{}'s balance: \x0f {}".format(args, monify(data[args.lower()][0]))
                except: 
                    if guessHost(args, data): returned  = "\x02{}'s balance: \x0f {}".format(guessHost(args, data), monify(data[guessHost(args, data)][0]))   #Guess the host
                    else: returned = "\x02[Error]\x0f Unknown hostmask '{}'".format(args)
    
    #THE STORE COMMAND FOR LISTING AND INFO. IF IT'S INFO RECRUSIVLY DO THIS COMMAND WITH INFO ARGUMENT
    elif t == "STORE":
        if args == "":
            returned = "Welcome to \x034\x02BowserBucks\x0f, do \x02{0}store list\x0f to see what's avaliable. Use \x02{0}info\x0f and \x02{0}buy <item> [amount]\x0f to get item info and purchase.".format(extra["config"].commandChar)
        elif args == "list":
            returned = ",".join(items.keys())
            
    elif t == "BUY":
        if args == "":
            raise Exception(hostmask + " had no args in buy.")
        thing = getHostData(hostmask, data)
        if thing == None: 
            returned = "Looks like you haven't registered yet, do \x02{}bal\x0f to do so!".format(extra["config"].commandChar)
        else:
            balance = data[hostmask.lower()][0] #Their user balance
            multiplier = 1 
            if len( args.split(" ") ) == 2: 
                try: multiplier = int( args.split(" ")[1].replace(",","") )
                except: return "\x02[Error]\x0f Invalid amount!"
            
            #Try to find the cost of the item the user is buying
            found = False
            for key in items:
                if items[key].name.lower() == args.split(" ")[0]: #Found it
                    found = True 
                    if items[key].cost*multiplier > balance: #Too damn expensive :P
                        returned = "\x02{}\x0f: You can't afford that!".format(user)
                    else:
                        if not items[key].buyable:
                            returned = "\x02{}\x0f: You can't buy that (Not buyable)!".format(user)
                        else:
                            data[hostmask.lower()][0] -= items[key].cost*multiplier #Subtract it from the balance
                            
                            if key not in data[hostmask.lower()][1].keys():
                                data[hostmask.lower()][1][key] = 0
                            data[hostmask.lower()][1][key] += multiplier 
                            returned = "\x02Success! \x0fYou bought {} {} for {}".format(
                                    multiplier, 
                                    items[key].name,
                                    monify( items[key].cost*multiplier )
                            )
            if not found:
                returned = "\x02[Error]\x0f Item '{}' not found.".format(args)
            
    elif t == "GIVE":
        if args == "":
            raise Exception( hostmask + " No args for give.")
    
    #MAKE MEH BALANCE VERY BIG!!!!!!!!!!!!!!!
    try: data["unaffiliated/bowserinator"][0] = 100000000000000000000000000000000000000000000000000000000000000
    except: pass

    file = open("Bowserbucks/capitalism.json", "w")
    file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')) )
    file.close()
    return returned
