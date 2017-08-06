import random, time, requests
from Trival import quiz_solver
from Trival import url_info
from Trival import stats

def tinyurl(url):
    """Makes shortened url with tinyurl"""
    try:
        tiny_url = "http://tinyurl.com/api-create.php?url={0}".format(url)
        page = requests.get(tiny_url).text
        return page
    except: return url
    
ascii_chars = list("!~#$%^&*()-+_\|}{[]/><~`:;")
no_url_chan = ["##powder-bots"]
        
def doCheck(channel, message, user, hostmask, extra):
    returned = None
    
    #TIMEBOMB HANDLING
    #==========================================================================================================
    if "They quickly rearm the bomb and throw it back at {} with just seconds on the clock!".format(extra["config"].nick).lower() in message.lower():
        returned = "$duck"
    elif "stuffs a bomb down {}'s pants".format(extra["config"].nick).lower() in message.lower():
        try:
            returned = random.choice( message.split("They are: ")[1].replace(", and",",").replace(".","").replace("and",",").split(",") )
            returned = "$cut " + returned.lstrip().rstrip().replace("\x01","".replace("\"",""))
        except:
            returned = '$cut potato'
    
    #QUIZ SOLVER 
    #==========================================================================================================
    if extra["config"].quizSolve and quiz_solver.phraseChat(message, user):
        returned = quiz_solver.phraseChat(message, user)
        time.sleep(1)
    
    #NO POKE
    #==========================================================================================================
    if "pokes " + extra["config"].nick.lower() in message.lower():
        returned = "\x01ACTION pokes " + user + ".\x01"
    
    #MOO RESPONDER
    #==========================================================================================================
    if message.lstrip().rstrip().lower() == "mooo":
        moo = "m" + "".join( ["\x03"+str(random.randint(0,15))+","+str(random.randint(0,15))+"o" for i in range(0,50)] ) + "!!!"
        returned = "\x02{}: {}".format(user, moo)
    
    #FUCK HANDICRAFTSMAN
    if "bowserinator" in message.lower() and "reset" in message.lower() and "perm" in message.lower() and user != "Bowserinator" and user != extra["config"].nick:
        returned = 'FUCK OFF YOU ASSHOLE'
        extra['ircsock'].remove(extra["channel"],user,"Fuck off >:(")  
        
    
    #url_info AND URL STUFF
    #==========================================================================================================
    if channel not in no_url_chan:
        if message.find("https://www.youtube.com") != -1 or message.find("http://www.youtube.com") != -1:
            data = url_info.getYoutube( message.replace(" ",""))
            returned = "\x02Youtube Video: \x0f" + data
            
        #Get tpt saves in format ~ or link
        elif message.find("powdertoy.co.uk/Browse/View.html?ID=") != -1:
            saveId = message.split("powdertoy.co.uk/Browse/View.html?ID=")[1].split(" ")[0]
            returned = url_info.getTPT(saveId)
            
        elif message.startswith("~"):
            saveId = message.split("~")[1].split(" ")[0]
            returned = url_info.getTPT(saveId)
            
        elif message.find("http://powdertoy.co.uk/Discussions/Thread/View.html?Thread=") != -1:
            saveId = message.split("http://powdertoy.co.uk/Discussions/Thread/View.html?Thread=")[1].split(" ")[0]
            returned = url_info.getThread(saveId)
            
        elif message.find("tpt.io/") != -1:
            saveId = message.split("tpt.io/")[1].split(" ")[0]
            returned = url_info.getThread(saveId)
                
        elif "http" in message:
            returned = url_info.getTitleURL(message).encode('utf8')
    
    #Update some stats
    #============================================================================================
    stats.parse( extra["ircmsg"], extra["config"] )
    
    #Stop jeffl35 from doing kbans :)
    if "-kick {}".format(extra["config"].nick).lower() in message.lower():
        time.sleep(0.5)
        returned = "Please visit " + tinyurl("https://dummyimage.com/600x400/000/fff&text=fuck+you+{}".format(user))
        extra["ircsock"].remove(extra["channel"],"otherbot","**Psychic power noise**")  
        extra["ircsock"].remove(extra["channel"],"otterbot","**Psychic power noise**") 
        
        time.sleep(6)
        extra["ircsock"].joinchan(extra["channel"]) 
        extra["ircsock"].sendmsg(extra["channel"],"Suprise motherfu*ka!") 
        
        
    if "-kban {}".format(extra["config"].nick).lower() in message.lower():
        time.sleep(0.5)
        returned = "Please visit " + tinyurl("https://dummyimage.com/600x400/000/fff&text=fuck+you+jeffl35" + "".join(["" for i in range(0,random.randint(1,10))]))
        extra["ircsock"].remove(extra["channel"],"otherbot","**Psychic power noise**")  
        extra["ircsock"].remove(extra["channel"],"otterbot","**Psychic power noise**")  
        
        #extra["ircsock"].sendmsg("ChanServ","deop {} {}".format(channel,"otterbot"))
        #extra["ircsock"].sendmsg("ChanServ","deop {} {}".format(channel,"otherbot"))
        
        extra["ircsock"].sendmsg("ChanServ","op {}".format(extra["channel"]))
        extra["ircsock"].remove(extra["channel"],user,"How do you like to be kicked?") 
        
        time.sleep(6)
        extra["ircsock"].joinchan(extra["channel"]) 
        extra["ircsock"].sendmsg(extra["channel"],"Suprise motherfu*ka!") 
        
    #Some more stuff
    if "slaps {}".format(extra["config"].nick).lower() in message.lower():
        returned = "\x01ACTION matrix dodges the slap!\x01"
    
    if "pocket" in hostmask and random.choice([True,False]) and "php" in message.lower():
        returned = random.choice([
            "Php: training wheels without the bike",
            "Php? No thanks, I don't do drugs",
            "I don't always use php... But when I do, I often need help.",
            "Php sucks sooo much!!",
            "Pocketkiller <3 php, wait... 09:28:54 <PocketKiller> php is shit ok"
        ])
    
    #Ruin ascii art
    #if len(message) > 5 and len(message.replace(" ","")) > 0 and len([i for i in message.replace(" ","") if i.lower() in ascii_chars]) / len(message.replace(" ","")) > 0.8:
        #returned = "YOUR ASCII ART IS RUINED!!!"
    
    if returned == "": returned = None
    if returned:
        extra["output"].append([channel, returned])
    return None