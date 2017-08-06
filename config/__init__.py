import sys, re, time, repl, subprocess, random
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
    
import commands
#TODO: kban, fkban, voice, unvoice, stab, unstab, unban, invite
r = repl.Repl()

@commands.add_cmd
def kickme(args,user="",hostmask="",extra={}):
    """kickme - Kick urself
    {"category":"op"}"""
    extra["ircsock"].kickuser( extra["channel"], user, "You asked for it!")
    return ""
    
@commands.add_cmd
def rawunban(args,user="",hostmask="",extra={}):
    """rawunban <nick|nicks|regex> channel - Unban a raw hostmask
    {"category":"op","permLevel":50,"threaded":false}"""
    channel = extra["channel"]
    if len(args.split(" ")) >= 2:
        channel = args.lstirp().rstrip().split(" ")[-1]
        args = args.split(channel)[0].lstrip().rstrip()
    
    extra["ircsock"].unban(channel, args)
    return ""

@commands.add_cmd
def unban(args,user="",hostmask="",extra={}):
    """unban <nick|nicks|regex> [channel] - Unban someone
    {"category":"op","permLevel":50,"threaded":false}"""
    
    return "NOT DONE YET - TODO: make it get bans and search for that match user"


@commands.add_cmd
def rawban(args,user="",hostmask="",extra={}):
    """rawban <nick|nicks|regex> channel - Ban a raw hostmask
    {"category":"op","permLevel":50,"threaded":false}"""
    channel = extra["channel"]
    if len(args.split(" ")) >= 2:
        channel = args.lstirp().rstrip().split(" ")[-1]
        args = args.split(channel)[0].lstrip().rstrip()
    
    extra["ircsock"].ban(channel, args)
    return ""

@commands.add_cmd
def ban(args,user="",hostmask="",extra={}):
    """ban <nick|nicks|regex> [channel] - Ban someone
    {"category":"op","permLevel":50,"threaded":false}"""
    channel = extra["channel"]
    if len(args.split(" ")) >= 2:
        channel = args.lstrip().rstrip().split(" ")[-1]
        args = args.split(channel)[0].lstrip().rstrip()
    
    affected = []
    if "*" in args: #Regex match
        names = getNamesChannel(channel, extra["ircsock"].ircsock)
        for i in names:
            if re.search( args.replace("*",".*?").lower(), i[0].lower()) and i[0] != extra["config"].nick:
                affected.append( i[0] )
    else:
        affected = args.split(",")
    affected = [ extra["ircsock"].getbanmask(n.lstrip().rstrip()) for n in affected]
    
    i = 0
    for x in range(0,len(affected)+1,4):
        try: extra["ircsock"].setMode( channel, " ".join([affected[x],affected[x+1],affected[x+2],affected[x+3]]), "+bbbb" )
        except: 
            try: extra["ircsock"].setMode( channel, " ".join([affected[x],affected[x+1],affected[x+2]]) , "+bbbb")
            except: 
                try: extra["ircsock"].setMode(channel, " ".join([affected[x],affected[x+1]]) , "+bbbb" )
                except: extra["ircsock"].setMode(channel, " ".join([affected[x]])  , "+bbbb")
        i+=1
        if i % 4 == 0: 
            time.sleep(0.7)
    return ""


@commands.add_cmd
def remove(args,user="",hostmask="",extra={}):
    """remove <nick> channel=[channel] [reason] - Remove someone from channel, they will view it as a PART.
    {"category":"op","permLevel":50,"threaded":false,"alias":["ninja"]}"""
    channel = extra["channel"]
    reason = "[Default kick reason here]"
    if "channel=" in args:
        channel = args.split("channel=")[1].split(" ")[0]
        args = args.replace("channel="+channel, "")
    if len(args.split(" ")) >= 2:
        reason = args.split(" ",1)[1]
        args = args.replace(reason,"")
        args = args.lstrip().rstrip()
    extra["ircsock"].remove( channel, args , reason )
    return ""
    
@commands.add_cmd
def removeme(args,user="",hostmask="",extra={}):
    """removeme - Remove urself
    {"category":"op","alias":["ninjame"]}"""
    channel = extra["channel"]
    reason = random.choice(["You asked for it!","Ok then","Cooler than kickme!","Thanks for not using otherbot!"])
    extra["ircsock"].remove( channel, user , reason )
    return ""
    
@commands.add_cmd
def trollkick(args,user="",hostmask="",extra={}):
    """trollkick <nick> channel=[channel] [reason] - Ban someone, kick them then quickly unban.
    {"category":"op","permLevel":50,"threaded":false}"""
    channel = extra["channel"]
    reason = "[Default kick reason here]"
    if "channel=" in args:
        channel = args.split("channel=")[1].split(" ")[0]
        args = args.replace("channel="+channel, "")
    if len(args.split(" ")) >= 2:
        reason = args.split(" ",1)[1]
        args = args.replace(reason,"")
        args = args.lstrip().rstrip()
    
    if args.lstrip().rstrip() == "":
        affected = [user]
    else:
        affected = args.split(",")
        affected = [n.lstrip().rstrip() for n in affected]
        
    x = 0
    for i in affected:
        ban = extra["ircsock"].getbanmask(i)
        extra["ircsock"].setMode(channel, "{} {}".format(i,ban) , "-o+b")
        extra["ircsock"].kickuser( channel, i, reason )
        time.sleep(2)
        extra["ircsock"].unban(channel, ban )
        x+=1
        if x % 4 == 0:
            time.sleep(0.7)
    return ""
        
@commands.add_cmd
def kick(args,user="",hostmask="",extra={}):
    """kick <nick|nicks|regex> channel=[channel] [reason] - Kick people out of the channel.
    {"category":"op","permLevel":50,"threaded":false}"""
    channel = extra["channel"]
    reason = "[Default kick reason here]"
    if "channel=" in args:
        channel = args.split("channel=")[1].split(" ")[0]
        args = args.replace("channel="+channel, "")
    if len(args.split(" ")) >= 2:
        reason = args.lstrip().rstrip().split(" ",1)[1]
        args = args.replace(reason,"")
        args = args.lstrip().rstrip()
    
    affected = []
    if "*" in args: #Regex match
        names = getNamesChannel(channel, extra["ircsock"].ircsock)
        for i in names:
            if re.search( args.replace("*",".*").lower(), i[0].lower()) and i[0] != extra["config"].nick:
                if i[0].encode('ascii').lower() not in ["366","/names","list", channel]:
                    affected.append( i[0].replace("\r","").encode('ascii') )
    elif args.lstrip().rstrip() == "":
        affected = [user]
    else:
        affected = args.split(",")
        affected = [n.lstrip().rstrip() for n in affected]
    
    x = 0
    for i in affected:
        extra["ircsock"].kickuser( channel, i, reason )
        x+=1
        if x % 4 == 0:
            time.sleep(0.7)
    return ""
    
@commands.add_cmd
def deop(args,user="",hostmask="",extra={}):
    """deop <nick|nicks|regex> <channel> - Deop people 
    {"category":"op","permLevel":50,"threaded":false}"""
    
    channel = extra["channel"]
    if len(args.split(" ")) >= 2:
        channel = args.lstrip().rstrip().split(" ")[-1]
        args = args.split(channel)[0].lstrip().rstrip()
    
    affected = []
    if "*" in args: #Regex match
        names = getNamesChannel(channel, extra["ircsock"].ircsock)
        for i in names:
            if i[1] == "op" and re.search( args.replace("*",".*?").lower(), i[0].lower()) and i[0] != extra["config"].nick:
                affected.append( i[0] )
    elif args.lstrip().rstrip() == "":
        affected = [user]
    else:
        affected = args.split(",")
        affected = [n.lstrip().rstrip() for n in affected]
    
    i = 0
    for x in range(0,len(affected)+1,4):
        try: extra["ircsock"].setMode( channel, " ".join([affected[x],affected[x+1],affected[x+2],affected[x+3]]) , "-oooo")
        except: 
            try: extra["ircsock"].setMode( channel, " ".join([affected[x],affected[x+1],affected[x+2]]) , "-oooo")
            except: 
                try: extra["ircsock"].setMode(channel, " ".join([affected[x],affected[x+1]]) , "-oooo")
                except: 
                    try: extra["ircsock"].setMode(channel, " ".join([affected[x]]) , "-oooo")
                    except: pass
        i+=1
        if i % 4 == 0: 
            time.sleep(0.7)
    return ""
    
@commands.add_cmd
def stab(args,user="",hostmask="",extra={}):
    """stab <nick|nicks|regex> <channel> - Make someone quieter...
    {"category":"op","permLevel":50,"threaded":false}"""
    
    channel = extra["channel"]
    if len(args.split(" ")) >= 2:
        channel = args.lstrip().rstrip().split(" ")[-1]
        args = args.split(channel)[0].lstrip().rstrip()
    
    affected = []
    if "*" in args: #Regex match
        names = getNamesChannel(channel, extra["ircsock"].ircsock)
        for i in names:
            if re.search( args.replace("*",".*?").lower(), i[0].lower()) and i[0] != extra["config"].nick:
                affected.append( i[0] )
    elif args.lstrip().rstrip() == "":
        affected = [user]
    else:
        affected = args.split(",")
        affected = [n.lstrip().rstrip() for n in affected]
    
    i = 0
    for x in range(0,len(affected)+1,4):
        try: extra["ircsock"].setMode( channel, " ".join([affected[x],affected[x+1],affected[x+2],affected[x+3]]) , "+qqqqq")
        except: 
            try: extra["ircsock"].setMode( channel, " ".join([affected[x],affected[x+1],affected[x+2]]) , "+qqqq")
            except: 
                try: extra["ircsock"].setMode(channel, " ".join([affected[x],affected[x+1]]) , "+qqqq")
                except: 
                    try: extra["ircsock"].setMode(channel, " ".join([affected[x]]) , "+qqqq")
                    except: pass
        i+=1
        if i % 4 == 0: 
            time.sleep(0.7)
    return ""
    
@commands.add_cmd
def unstab(args,user="",hostmask="",extra={}):
    """unstab <nick|nicks|regex> <channel> - Unquiet someone
    {"category":"op","permLevel":50,"threaded":false}"""
    
    channel = extra["channel"]
    if len(args.split(" ")) >= 2:
        channel = args.lstrip().rstrip().split(" ")[-1]
        args = args.split(channel)[0].lstrip().rstrip()
    
    affected = []
    if "*" in args: #Regex match
        names = getNamesChannel(channel, extra["ircsock"].ircsock)
        for i in names:
            if re.search( args.replace("*",".*?").lower(), i[0].lower()) and i[0] != extra["config"].nick:
                affected.append( i[0] )
    elif args.lstrip().rstrip() == "":
        affected = [user]
    else:
        affected = args.split(",")
        affected = [n.lstrip().rstrip() for n in affected]
    
    i = 0
    for x in range(0,len(affected)+1,4):
        try: extra["ircsock"].setMode( channel, " ".join([affected[x],affected[x+1],affected[x+2],affected[x+3]]) , "-qqqq")
        except: 
            try: extra["ircsock"].setMode( channel, " ".join([affected[x],affected[x+1],affected[x+2]]) , "-qqqq")
            except: 
                try: extra["ircsock"].setMode(channel, " ".join([affected[x],affected[x+1]]) , "-qqqq")
                except: 
                    try: extra["ircsock"].setMode(channel, " ".join([affected[x]]) , "-qqqq")
                    except: pass
        i+=1
        if i % 4 == 0: 
            time.sleep(0.7)
    return ""
    
@commands.add_cmd
def voice(args,user="",hostmask="",extra={}):
    """voice <nick|nicks|regex> <channel> - Voice people 
    {"category":"op","permLevel":50,"threaded":false}"""
    
    channel = extra["channel"]
    if len(args.split(" ")) >= 2:
        channel = args.lstrip().rstrip().split(" ")[-1]
        args = args.split(channel)[0].lstrip().rstrip()
    
    affected = []
    if "*" in args: #Regex match
        names = getNamesChannel(channel, extra["ircsock"].ircsock)
        for i in names:
            if re.search( args.replace("*",".*?").lower(), i[0].lower()) and i[0] != extra["config"].nick:
                affected.append( i[0] )
    elif args.lstrip().rstrip() == "":
        affected = [user]
    else:
        affected = args.split(",")
        affected = [n.lstrip().rstrip() for n in affected]
    
    i = 0
    for x in range(0,len(affected)+1,4):
        try: extra["ircsock"].setMode( channel, " ".join([affected[x],affected[x+1],affected[x+2],affected[x+3]]) , "+vvvv")
        except: 
            try: extra["ircsock"].setMode( channel, " ".join([affected[x],affected[x+1],affected[x+2]]) , "+vvvv")
            except: 
                try: extra["ircsock"].setMode(channel, " ".join([affected[x],affected[x+1]]) , "+vvvv")
                except: 
                    try: extra["ircsock"].setMode(channel, " ".join([affected[x]]) , "+vvvv")
                    except: pass
        i+=1
        if i % 4 == 0: 
            time.sleep(0.7)
    return ""
    
@commands.add_cmd
def devoice(args,user="",hostmask="",extra={}):
    """devoice <nick|nicks|regex> <channel> - DeVoice people 
    {"category":"op","permLevel":50,"threaded":false}"""
    
    channel = extra["channel"]
    if len(args.split(" ")) >= 2:
        channel = args.lstrip().rstrip().split(" ")[-1]
        args = args.split(channel)[0].lstrip().rstrip()
    
    affected = []
    if "*" in args: #Regex match
        names = getNamesChannel(channel, extra["ircsock"].ircsock)
        for i in names:
            if re.search( args.replace("*",".*?").lower(), i[0].lower()) and i[0] != extra["config"].nick:
                affected.append( i[0] )
    elif args.lstrip().rstrip() == "":
        affected = [user]
    else:
        affected = args.split(",")
        affected = [n.lstrip().rstrip() for n in affected]
    
    i = 0
    for x in range(0,len(affected)+1,4):
        try: extra["ircsock"].setMode( channel, " ".join([affected[x],affected[x+1],affected[x+2],affected[x+3]]) , "-vvvv")
        except: 
            try: extra["ircsock"].setMode( channel, " ".join([affected[x],affected[x+1],affected[x+2]]) , "-vvvv")
            except: 
                try: extra["ircsock"].setMode(channel, " ".join([affected[x],affected[x+1]]) , "-vvvv")
                except: 
                    try: extra["ircsock"].setMode(channel, " ".join([affected[x]]) , "-vvvv")
                    except: pass
        i+=1
        if i % 4 == 0: 
            time.sleep(0.7)
    return ""
    
@commands.add_cmd
def op(args,user="",hostmask="",extra={}):
    """op <nick|nicks|regex> <channel> - Op people 
    {"category":"op","permLevel":50,"threaded":false}"""
    
    channel = extra["channel"]
    if len(args.split(" ")) >= 2:
        channel = args.lstrip().rstrip().split(" ")[-1]
        args = args.split(channel)[0].lstrip().rstrip()
    
    affected = []
    if "*" in args: #Regex match
        names = getNamesChannel(channel, extra["ircsock"].ircsock)
        for i in names:
            if i[1] != "op" and re.search( args.replace("*",".*").lower(), i[0].lower()) and i[0] != extra["config"].nick:
                affected.append( i[0] )
    elif args.lstrip().rstrip() == "":
        affected = [user]
    else:
        affected = args.split(",")
        affected = [n.lstrip().rstrip() for n in affected]
    i = 0
    for x in range(0,len(affected)+1,4):
        try: extra["ircsock"].setMode( channel, " ".join([affected[x],affected[x+1],affected[x+2],affected[x+3]]) , "+oooo")
        except: 
            try: extra["ircsock"].setMode( channel, " ".join([affected[x],affected[x+1],affected[x+2]]) , "+oooo")
            except: 
                try: extra["ircsock"].setMode(channel, " ".join([affected[x],affected[x+1]]) , "+oooo")
                except: 
                    try: extra["ircsock"].setMode(channel, " ".join([affected[x]]) , "+oooo")
                    except: pass
        i+=1
        if i % 4 == 0: 
            time.sleep(0.7)
    return ""
        
def getNamesChannel(channel,irc):
    #Returns list of names in an array [["name","op"]]
    irc.send("NAMES {0}\r\n".format(channel).encode("UTF-8"))
    ircmsg = irc.recv(2048)
    ircmsg = ircmsg.decode("UTF-8")
    ircmsg = ircmsg.strip("\r\n")
    ircmsg = ircmsg.strip(":").split(" :",1)[1].split(" ")
    
    returned = []
    for i in ircmsg:
        if i.startswith("@"):
            returned.append([i.replace("@","",1), "op" ])
        elif i.startswith("+"):
            returned.append([i.replace("+","",1), "voice" ])
        else:
            returned.append([i,"none"])
    return returned
    

#Basic join part thing
@commands.add_cmd
def join(args,user="",hostmask="",extra={}):
    """join <channel> - Join a channel
    {"category":"op","permLevel":100}"""
    extra["ircsock"].joinchan(args)
    return "Joining {}...".format(args)
    
@commands.add_cmd
def cycle(args,user="",hostmask="",extra={}):
    """cycle [channel] - PART and JOIN a channel
    {"category":"op","permLevel":100}"""
    if args.lstrip().rstrip() == "":
        extra["ircsock"].partchan( extra["channel"] )
        extra["ircsock"].joinchan( extra["channel"] )
    else:
        extra["ircsock"].partchan(args)
        extra["ircsock"].joinchan(args)
    return ""

@commands.add_cmd
def part(args,user="",hostmask="",extra={}):
    """part [channel] - Part a channel
    {"category":"op","permLevel":100}"""
    if args.lstrip().rstrip() == "":
        extra["ircsock"].partchan( extra["channel"] )
    else:
        extra["ircsock"].partchan(args)
    return ""

#Enable or disable certain settings
#================================================================================
#================================================================================
@commands.add_cmd
def enablePM(args,user="",hostmask="",extra={}):
    """enablePM [true/false] - Toggle PM
    {"category":"config","permLevel":100}"""
    
    args = args.lstrip().rstrip().lower()
    if args == "":
        extra["config"].enablePM = not extra["config"].enablePM 
        return "\x02[Success!]\x0f enablePM toggled to {}".format( extra["config"].enablePM )
    elif args == "false":
        extra["config"].enablePM = False
        return "\x02[Success!]\x0f enablePM toggled to {}".format( extra["config"].enablePM )
    elif args == "true":
        extra["config"].enablePM = True
        return "\x02[Success!]\x0f enablePM toggled to {}".format( extra["config"].enablePM )
    return "\x02[Error] \x0fInvalid args!"
    
@commands.add_cmd
def unsafecommandchar(args,user="",hostmask="",extra={}):
    """unsafecommandchar [true/false] - Toggle PM
    {"category":"config","permLevel":100}"""
    
    args = args.lstrip().rstrip().lower()
    if args == "":
        extra["config"].unsafeCommandChar = not extra["config"].unsafeCommandChar 
        return "\x02[Success!]\x0f unsafecommandchar toggled to {}".format( extra["config"].unsafeCommandChar )
    elif args == "false":
        extra["config"].unsafeCommandChar = False
        return "\x02[Success!]\x0f unsafecommandchar toggled to {}".format( extra["config"].unsafeCommandChar )
    elif args == "true":
        extra["config"].unsafeCommandChar = True
        return "\x02[Success!]\x0f unsafecommandchar toggled to {}".format( extra["config"].unsafeCommandChar )
    return "\x02[Error] \x0fInvalid args!"

@commands.add_cmd
def quit(args="",user=None,hostmask=None,extra={}):
    """quit [message] - Quit the IRC server
    {"category":"config","permLevel":100}"""
    if args.lstrip().rstrip() == "":
        args = "Free will is an illusion. It is synonymous with incomplete perception."
    extra["ircsock"].quit(args)
    
@commands.add_cmd
def masshighlight(args="",user=None,hostmask=None,extra={}):
    """masshighlight - Masshighlight everyone
    {"category":"op","permLevel":100,"exist":false}"""
    users = getNamesChannel(extra["channel"],extra["ircsock"].ircsock)
    returned = ""
    for i in users:
        returned = returned + i[0] + " "
    extra["ircsock"].sendmsg(extra["channel"],returned)
    return ""

@commands.add_cmd
def py(args="",user=None,hostmask=None,extra={}):
    """py <code> - Run python code (NOT SANDBOXED)
    {"category":"config","permLevel":100}"""
    r.run("import commands")
    
    returned = str(r.run(args))
    if returned == None or returned.replace(" ","") == "": return "[No output]"
    return returned

@commands.add_cmd
def shell(args="",user=None,hostmask=None,extra={}): #+" | ./ircize --remove"
    """shell <code> - Run shell code
    {"category":"config","permLevel":100}"""
    try: 
        s = subprocess.check_output(args, stderr=subprocess.STDOUT, shell=True) 
    except: 
        return "An error has occured."
    if s: 
        s = s.decode() 
        for line in str(s).splitlines(): 
            extra["ircsock"].sendmsg(extra["channel"], line) 
    return ""