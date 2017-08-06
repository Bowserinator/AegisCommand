import art
import sys, time, socket
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import commands, requests, re, random, time
from HTMLParser import HTMLParser

roulette_chambers = [False,False,False,False,False,True]

@commands.add_cmd
def echo(args, user="",hostmask="",extra={}):
    """echo <text> - echo text
    {"category":"trivial"}"""
    return " " + args
    

@commands.add_cmd
def mooify(args, user="",hostmask="",extra={}):
    """mooify <user> - mooify a user.
    {"category":"trivial"}"""
    if args.lower() == "bowserinator":
        args = user
    return "\x01ACTION turns {} into a moo\x01".format(args)
    
    
@commands.add_cmd
def ascii(args, user="",hostmask="",extra={}):
    """ascii <art> - Draw ascii art :)
    {"category":"trivial","permLevel":100}"""
    args = args.lstrip().rstrip()
    if args == "":
        return "\x02Categories: \x0f" + ", ".join([item for item in eval("dir(art)") if not item.startswith("__")])
    else:
        try: 
            art = eval('art.'+args.lower())
            for line in art.split("\n"):
                extra["ircsock"].sendmsg(extra['channel'], line)
                time.sleep(1)
            return ""
        except:
            return "\x02Categories: \x0f" + ", ".join([item for item in eval("dir(art)") if not item.startswith("__")])
    return ""
    
    
@commands.add_cmd
def lorem(args, user="",hostmask="",extra={}):
    """lorem - Generate some lorem ipsum. 
    {"category":"trivial"}"""
    words = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetuer",
        "adipiscing", "elit", "sed", "diam", "nonummy", "nibh", "euismod",
        "tincidunt", "ut", "laoreet", "dolore", "magna", "aliquam", "erat"]
    return " ".join([ random.choice(words) for i in range(5,12)]).capitalize() + "."
        
@commands.add_cmd
def compliment(args, user="",hostmask="",extra={}):
    """compliment [user] - Compliment a user
    {"category":"trivial"}"""
    if args.lstrip().rstrip() == "":
        u = user
    else: 
        u = args
    h = HTMLParser()
    data = requests.get("http://www.complimentgenerator.co.uk/").text.replace("\n","")
    return "\x02"+u+"\x0f: " + h.unescape(re.findall('<p class="medium">(.*?)</p>', data)[0].replace(":","",1).lstrip().rstrip()).encode('utf8')

@commands.add_cmd
def blame(args, user="",hostmask="",extra={}):
    """blame <user> - blame a user
    {"category":"trivial"}"""
    return "\x01ACTION blames {}\x01".format(args)
    
@commands.add_cmd
def insult(args, user="",hostmask="",extra={}):
    """insult [user] - Insult a user
    {"category":"trivial","permLevel":100}"""
    #return "Disabled for being too insulting. How ironic."
    if args.lstrip().rstrip() == "":
        u = user
    else: 
        u = args
    h = HTMLParser()
    data = requests.get("http://www.insultgenerator.org/").text.replace("\n","")
    return "\x02"+u+"\x0f: " + h.unescape(re.findall('<div class="wrap">(.*?)</div>', data)[0].replace(":","",1).lstrip().rstrip()).encode('utf8').replace("<br>","")


    
    
@commands.add_cmd
def quizCheat(args,user="",hostmask="",extra={}):
    """quizCheat [true/false] - Toggle quizCheat
    {"category":"config","permLevel":100,"exist":false}"""
    
    args = args.lstrip().rstrip().lower()
    if args == "":
        extra["config"].quizSolve = not extra["config"].quizSolve 
        return "\x02[Success!]\x0f quizCheat toggled to {}".format( extra["config"].quizSolve )
    elif args == "false":
        extra["config"].quizSolve = False
        return "\x02[Success!]\x0f quizCheat toggled to {}".format( extra["config"].quizSolve )
    elif args == "true":
        extra["config"].quizSolve = True
        return "\x02[Success!]\x0f quizCheat toggled to {}".format( extra["config"].quizSolve )
    return "\x02[Error] \x0fInvalid args!"
    
@commands.add_cmd
def heil(args,user="",hostmask="",extra={}):
    """heil - ALL HAIL BOWSERINATOR 
    {"category":"trivial"}"""
    return "HEIL BOWSERINATOR!"

def scrambled(orig):
    dest = orig[:]
    random.shuffle(dest)
    return dest
    
@commands.add_cmd
def roulette(args,user="",hostmask="",extra={}):
    """roulette <user> [Odds of death as decimal]- Play russian roulette! There are 6 chambers, 1 bullet by default.
    {"category":"trivial"}"""
    args = args.lstrip().rstrip().lower()
    if args.lstrip().rstrip() == "":
        args = user
    if not commands.userPerms.get(hostmask,0) >= 30 and args != user:    
        return "You're not allowed to roulette someone else."
    elif args.lower() == commands.nick.lower():
        return "You can't roulette me!"
    
    args = args.split(" ")
    global roulette_chambers
    roulette_chambers = scrambled(roulette_chambers)
    if len(roulette_chambers) == 0: #Reload
        roulette_chambers = [False,False,False,False,False,True]
        extra["ircsock"].sendmsg(extra["channel"],"Reloading gun...")
        time.sleep(1)

    if len(args) <= 1:
        x = random.randint(0,len(roulette_chambers)-1)
        if roulette_chambers[x] == True:
            del roulette_chambers[x]
            extra["ircsock"].kickuser( extra["channel"], args[0], "You shot yourself. Ded XD" )
            roulette_chambers = [False,False,False,False,False,True]
            return "Reloading gun..."
        else:
            del roulette_chambers[x]
            return "*click* Nothing happens."
            
    elif len(args) == 2:
        try:
            if "/" in args[1]:
                args[1] = float(args[1].split("/")[0]) / float(args[1].split("/")[1])
            else:
                args[1] = float(args[1])
            if args[1] <= 0 or args[1] > 1:
                return "Invalid odds!!"
            if random.random() <= args[1]:
                extra["ircsock"].kickuser( extra["channel"], args[0], "You shot yourself. Ded XD" )
                return "Ded XD."
            else:
                return "They live to see another day."
        except:
            pass
    return "Invalid arguments found."
    
@commands.add_cmd
def poke(args,user="",hostmask="",extra={}):
    """poke <user> - Poke a user 
    {"category":"trivial"}"""
    
    args = args.lstrip().rstrip()
    if args == "":
        message = "pokes {} for not knowing how to use the poke command.".format(user)
    elif args.lower() == commands.nick.lower():
        args = args.split(" ")[0]
        message = "pokes {} for expecting {} to poke itself.".format(user, commands.nick)
    elif args.lower() == "bowserinator":
        args = args.split(" ")[0]
        message = "pokes {} for expecting {} to poke Bowserinator.".format(user, commands.nick)
    else:
        args = args.split(" ")[0]
        message = "pokes {}".format(args)
    return "\x01ACTION " + message + "\x01"


@commands.add_cmd
def gravbox(args,user="",hostmask="",extra={}):
    """gravbox [code, new lines are \\n] - Run gravbox code. 
    {"category":"trivial"}"""
    args = args.replace("\\n","\n")
    return "\x02Result: \x0f" + run( args, 1).replace("\n","").replace("\r","")
    
    
import random, time

def run( code, timeout = 999999 ): #Runs code
    start = time.time()
    stack = [] #The output stack 
    grav_direction = 0 #0 is down 1 is right 2 is up 3 is left
    quit = False
    returned = ""
    
    if "`" not in code:
        return "No ball found."
    elif "~" not in code:
        return "No return found."
    code = [list(c) for c in code.split("\n")]
        
    ball_cords = [] #Get the coordinates of all the balls
    for y in range(0, len(code)):
        for x in range(0, len(code[y])):
            if code[y][x] == "`":
                ball_cords.append([x,y])
                
    while not quit:
        #Update all the ball coordinates, run commands as hit
        for c in range(0,len(ball_cords)):
            if grav_direction == 0: #Down gravity
                try: 
                    if code[ball_cords[c][1] + 1][ball_cords[c][0]] == "#": pass
                    else: ball_cords[c][1] += 1
                except Exception as e: 
                    ball_cords[c][1] += 1
            elif grav_direction == 1: #Right gravity
                try: 
                    if code[ball_cords[c][1]][ball_cords[c][0] + 1] == "#": pass
                    else: ball_cords[c][0] += 1
                except Exception as e: 
                    ball_cords[c][0] += 1
            elif grav_direction == 2: #Up gravity
                try: 
                    if code[ball_cords[c][1] - 1][ball_cords[c][0]] == "#": pass
                    else: ball_cords[c][1] -= 1
                except Exception as e: 
                    ball_cords[c][1] -= 1
            elif grav_direction == 3: #Left gravity
                try: 
                    if code[ball_cords[c][1]][ball_cords[c][0] - 1] == "#": pass
                    else: ball_cords[c][0] -= 1
                except Exception as e: 
                    ball_cords[c][0] -= 1
                    
            if time.time() - start > timeout*1000:
                return "TIMEOUT"
        
        for x in range(0,len(ball_cords)): #Run commands:
            c = ball_cords[x]
            try:
                cmd = code[c[1]][c[0]]
                if cmd == "@": #Counter-clockwise switch gravity
                    grav_direction = (grav_direction+1)%4
                elif cmd == "/": #Bounce right
                    ball_cords[x][0] += 1
                elif cmd == "\\": #Bounce left
                    ball_cords[x][0] -= 1
                elif cmd == "!": #Invert stack item
                    if int(stack[0]) == stack[0]:
                        stack[0] =  stack[0]*-1 
                    else: pass 
                elif cmd in "1234567890": #Add number to stack
                    stack.append( int(cmd) )
                elif cmd == "+":
                    try: 
                        stack.append( int(stack[0]) + int(stack[1]) )
                        del stack[0]; del stack[0]
                    except: pass
                elif cmd == "-":
                    try: 
                        stack.append( int(stack[0]) - int(stack[1]) )
                        del stack[0]; del stack[0]
                    except: pass
                elif cmd == "*":
                    try: 
                        stack.append( int(stack[0]) * int(stack[1]) )
                        del stack[0]; del stack[0]
                    except: pass
                elif cmd == "|":
                    try: 
                        stack.append( int(stack[0]) / int(stack[1]) )
                        del stack[0]; del stack[0]
                    except: pass
                elif cmd == ".":
                    try: 
                        if type(stack[-1]) == int:
                           returned += chr(stack[-1])
                        else:
                            returned += stack[-1]
                        del stack[-1]
                    except: pass
                elif cmd == "^":
                    try: stack.append( stack[0] )
                    except: pass
                elif cmd == "%":
                    try: del stack[0]
                    except: pass
                elif cmd.lower() in "abcdefghijklmnopqrstuvwxyz":
                    stack.append(cmd)
                elif cmd == "?":
                    ball_cords[x][0] += random.choice([-1,1])
                elif cmd == "&":
                    try:
                        if stack[0] > 0:
                            ball_cords[x][0] += 1
                        else: 
                            ball_cords[x][0] -= 1
                    except: pass
                elif cmd == "$":
                    stack.append( len(stack) )
                elif cmd == "~":
                    quit = True
                elif cmd == ":":
                    try:
                        stack[0],stack[-1] = stack[-1],stack[0]
                    except: pass

                #code[c[1]][c[0]] = "" #Destroy the command!
            except: #Code index doesn't exist!!
                pass
        
        if time.time() - start > timeout*1000:
            return "TIMEOUT"
        #quit = True
                
    return returned
    
    
excuses = ["clock speed",
"solar flares",
"electromagnetic radiation from satellite debris",
"static from nylon underwear",
"static from plastic slide rules",
"global warming",
"poor power conditioning",
"static buildup",
"doppler effect",
"hardware stress fractures",
"magnetic interference from money/credit cards",
"dry joints on cable plug",
"we're waiting for [the phone company] to fix that line",
"sounds like a Windows problem, try calling Microsoft support",
"temporary routing anomaly",
"somebody was calculating pi on the server",
"fat electrons in the lines",
"excess surge protection",
"floating point processor overflow",
"divide-by-zero error",
"POSIX compliance problem",
"monitor resolution too high",
"improperly oriented keyboard",
"network packets travelling uphill (use a carrier pigeon)",
"Decreasing electron flux",
"first Saturday after first full moon in Winter",
"radiosity depletion",
"CPU radiator broken",
"It works the way the Wang did, what's the problem",
"positron router malfunction",
"cellular telephone interference",
"techtonic stress",
"piezo-electric interference",
"(l)user error",
"working as designed",
"dynamic software linking table corrupted",
"heavy gravity fluctuation, move computer to floor rapidly",
"secretary plugged hairdryer into UPS",
"terrorist activities",
"not enough memory, go get system upgrade",
"interrupt configuration error",
"spaghetti cable cause packet failure",
"boss forgot system password",
"bank holiday - system operating credits  not recharged",
"virus attack, luser responsible",
"waste water tank overflowed onto computer",
"Complete Transient Lockout",
"bad ether in the cables",
"Bogon emissions",
"Change in Earth's rotational speed",
"Cosmic ray particles crashed through the hard disk platter",
"Smell from unhygienic janitorial staff wrecked the tape heads",
"Little hamster in running wheel had coronary; waiting for replacement to be Fedexed from Wyoming",
"Evil dogs hypnotised the night shift",
"Plumber mistook routing panel for decorative wall fixture",
"Electricians made popcorn in the power supply",
"Groundskeepers stole the root password",
"high pressure system failure",
"failed trials, system needs redesigned",
"system has been recalled",
"not approved by the FCC",
"need to wrap system in aluminum foil to fix problem",
"not properly grounded, please bury computer",
"CPU needs recalibration",
"system needs to be rebooted",
"bit bucket overflow",
"descramble code needed from software company",
"only available on a need to know basis",
"knot in cables caused data stream to become twisted and kinked",
"nesting roaches shorted out the ether cable",
"The file system is full of it",
"Satan did it",
"Daemons did it",
"You're out of memory",
"There isn't any problem",
"Unoptimized hard drive",
"Typo in the code",
"Yes, yes, its called a design limitation",
"Look, buddy:  Windows 3.1 IS A General Protection Fault.",
"That's a great computer you have there; have you considered how it would work as a BSD machine?",
"Please excuse me, I have to circuit an AC line through my head to get this database working.",
"Yeah, yo mama dresses you funny and you need a mouse to delete files.",
"Support staff hung over, send aspirin and come back LATER.",
"Someone is standing on the ethernet cable, causing a kink in the cable",
"Windows 95 undocumented \"feature\"",
"Runt packets",
"Password is too complex to decrypt",
"Boss' kid fucked up the machine",
"Electromagnetic energy loss",
"Budget cuts",
"Mouse chewed through power cable",
"Stale file handle (next time use Tupperware(tm)!)",
"Feature not yet implemented",
"Internet outage",
"Pentium FDIV bug",
"Vendor no longer supports the product",
"Small animal kamikaze attack on power supplies",
"The vendor put the bug there.",
"SIMM crosstalk.",
"IRQ dropout",
"Collapsed Backbone",
"Power company testing new voltage spike (creation) equipment",
"operators on strike due to broken coffee machine",
"backup tape overwritten with copy of system manager's favourite CD",
"UPS interrupted the server's power",
"The electrician didn't know what the yellow cable was so he yanked the ethernet out.",
"The keyboard isn't plugged in",
"The air conditioning water supply pipe ruptured over the machine room",
"The electricity substation in the car park blew up.",
"The rolling stones concert down the road caused a brown out",
"The salesman drove over the CPU board.",
"The monitor is plugged into the serial port",
"Root nameservers are out of sync",
"electro-magnetic pulses from French above ground nuke testing.",
"your keyboard's space bar is generating spurious keycodes.",
"the real ttys became pseudo ttys and vice-versa.",
"the printer thinks its a router.",
"the router thinks its a printer.",
"evil hackers from Serbia.",
"we just switched to FDDI.",
"halon system went off and killed the operators.",
"because Bill Gates is a Jehovah's witness and so nothing can work on St. Swithin's day.",
"user to computer ratio too high.",
"user to computer ration too low.",
"we just switched to Sprint.",
"it has Intel Inside",
"Sticky bits on disk.",
"Power Company having EMP problems with their reactor",
"The ring needs another token",
"new management",
"telnet: Unable to connect to remote host: Connection refused",
"SCSI Chain overterminated",
"It's not plugged in.",
"because of network lag due to too many people playing deathmatch",
"You put the disk in upside down.",
"Daemons loose in system.",
"User was distributing pornography on server; system seized by FBI.",
"BNC (brain not connected)",
"UBNC (user brain not connected)",
"LBNC (luser brain not connected)",
"disks spinning backwards - toggle the hemisphere jumper.",
"new guy cross-connected phone lines with ac power bus.",
"had to use hammer to free stuck disk drive heads.",
"Too few computrons available.",
"Flat tire on station wagon with tapes.  (\"Never underestimate the bandwidth of a station wagon full of tapes hurling down the highway\" Andrew S. Tannenbaum) ",
"Communications satellite used by the military for star wars.",
"Party-bug in the Aloha protocol.",
"Insert coin for new game",
"Dew on the telephone lines.",
"Arcserve crashed the server again.",
"Some one needed the powerstrip, so they pulled the switch plug.",
"My pony-tail hit the on/off switch on the power strip.",
"Big to little endian conversion error",
"You can tune a file system, but you can't tune a fish (from most tunefs man pages)",
"Dumb terminal",
"Zombie processes haunting the computer",
"Incorrect time synchronization",
"Defunct processes",
"Stubborn processes",
"non-redundant fan failure ",
"monitor VLF leakage",
"bugs in the RAID",
"no \"any\" key on keyboard",
"root rot",
"Backbone Scoliosis",
"/pub/lunch",
"excessive collisions & not enough packet ambulances",
"le0: no carrier: transceiver cable problem?",
"broadcast packets on wrong frequency",
"popper unable to process jumbo kernel",
"NOTICE: alloc: /dev/null: filesystem full",
"pseudo-user on a pseudo-terminal",
"Recursive traversal of loopback mount points",
"Backbone adjustment",
"OS swapped to disk",
"vapors from evaporating sticky-note adhesives",
"sticktion",
"short leg on process table",
"multicasts on broken packets",
"ether leak",
"Atilla the Hub",
"endothermal recalibration",
"filesystem not big enough for Jumbo Kernel Patch",
"loop found in loop in redundant loopback",
"system consumed all the paper for paging",
"permission denied",
"Reformatting Page. Wait...",
"..disk or the processor is on fire.",
"SCSI's too wide.",
"Proprietary Information.",
"Just type 'mv * /dev/null'.",
"runaway cat on system.",
"Did you pay the new Support Fee?",
"We only support a 1200 bps connection.",
"We only support a 28000 bps connection.",
"Me no internet, only janitor, me just wax floors.",
"I'm sorry a pentium won't do, you need an SGI to connect with us.",
"Post-it Note Sludge leaked into the monitor.",
"the curls in your keyboard cord are losing electricity.",
"The monitor needs another box of pixels.",
"RPC_PMAP_FAILURE",
"kernel panic: write-only-memory (/dev/wom0) capacity exceeded.",
"Write-only-memory subsystem too slow for this machine. Contact your local dealer.",
"Just pick up the phone and give modem connect sounds. \"Well you said we should get more lines so we don't have voice lines.\"",
"Quantum dynamics are affecting the transistors",
"Police are examining all internet packets in the search for a narco-net-trafficker",
"We are currently trying a new concept of using a live mouse.  Unfortunately, one has yet to survive being hooked up to the computer.....please bear with us.",
"Your mail is being routed through Germany ... and they're censoring us.",
"Only people with names beginning with 'A' are getting mail this week (a la Microsoft)",
"We didn't pay the Internet bill and it's been cut off.",
"Lightning strikes.",
"Of course it doesn't work. We've performed a software upgrade.",
"Change your language to Finnish.",
"Fluorescent lights are generating negative ions. If turning them off doesn't work, take them out and put tin foil on the ends.",
"High nuclear activity in your area.",
"What office are you in? Oh, that one.  Did you know that your building was built over the universities first nuclear research site? And wow, aren't you the lucky one, your office is right over where the core is buried!",
"The MGs ran out of gas.",
"The UPS doesn't have a battery backup.",
"Recursivity.  Call back if it happens again.",
"Someone thought The Big Red Button was a light switch.",
"The mainframe needs to rest.  It's getting old, you know.",
"I'm not sure.  Try calling the Internet's head office -- it's in the book.",
"The lines are all busy (busied out, that is -- why let them in to begin with?).",
"Jan  9 16:41:27 huber su: 'su root' succeeded for .... on /dev/pts/1",
"It's those computer people in X {city of world}.  They keep stuffing things up.",
"A star wars satellite accidently blew up the WAN.",
"Fatal error right in front of screen",
"That function is not currently supported, but Bill Gates assures us it will be featured in the next upgrade.",
"wrong polarity of neutron flow",
"Lusers learning curve appears to be fractal",
"We had to turn off that service to comply with the CDA Bill.",
"Ionization from the air-conditioning",
"TCP/IP UDP alarm threshold is set too low.",
"Someone is broadcasting pygmy packets and the router doesn't know how to deal with them.",
"The new frame relay network hasn't bedded down the software loop transmitter yet. ",
"Fanout dropping voltage too much, try cutting some of those little traces",
"Plate voltage too low on demodulator tube",
"You did wha... oh _dear_....",
"CPU needs bearings repacked",
"Too many little pins on CPU confusing it, bend back and forth until 10-20% are neatly removed. Do _not_ leave metal bits visible!",
"_Rosin_ core solder? But...",
"Software uses US measurements, but the OS is in metric...",
"The computer fleetly, mouse and all.",
"Your cat tried to eat the mouse.",
"The Borg tried to assimilate your system. Resistance is futile.",
"It must have been the lightning storm we had (yesterday) (last week) (last month)",
"Due to Federal Budget problems we have been forced to cut back on the number of users able to access the system at one time. (namely none allowed....)",
"Too much radiation coming from the soil.",
"Unfortunately we have run out of bits/bytes/whatever. Don't worry, the next supply will be coming next week.",
"Program load too heavy for processor to lift.",
"Processes running slowly due to weak power supply",
"Our ISP is having {switching,routing,SMDS,frame relay} problems",
"We've run out of licenses",
"Interference from lunar radiation",
"Standing room only on the bus.",
"You need to install an RTFM interface.",
"That would be because the software doesn't work.",
"That's easy to fix, but I can't be bothered.",
"Someone's tie is caught in the printer, and if anything else gets printed, he'll be in it too.",
"We're upgrading /dev/null",
"The Usenet news is out of date",
"Our POP server was kidnapped by a weasel.",
"It's stuck in the Web.",
"Your modem doesn't speak English.",
"The mouse escaped.",
"All of the packets are empty.",
"The UPS is on strike.",
"Neutrino overload on the nameserver",
"Melting hard drives",
"Someone has messed up the kernel pointers",
"The kernel license has expired",
"Netscape has crashed",
"The cord jumped over and hit the power switch.",
"It was OK before you touched it.",
"Bit rot",
"U.S. Postal Service",
"Your Flux Capacitor has gone bad.",
"The Dilithium Crystals need to be rotated.",
"The static electricity routing is acting up...",
"Traceroute says that there is a routing problem in the backbone.  It's not our problem.",
"The co-locator cannot verify the frame-relay gateway to the ISDN server.",
"High altitude condensation from U.S.A.F prototype aircraft has contaminated the primary subnet mask. Turn off your computer for 9 days to avoid damaging it.",
"Lawn mower blade in your fan need sharpening",
"Electrons on a bender",
"Telecommunications is upgrading. ",
"Telecommunications is downgrading.",
"Telecommunications is downshifting.",
"Hard drive sleeping. Let it wake up on it's own...",
"Interference between the keyboard and the chair.",
"The CPU has shifted, and become decentralized.",
"Due to the CDA, we no longer have a root account.",
"We ran out of dial tone and we're and waiting for the phone company to deliver another bottle.",
"You must've hit the wrong any key.",
"PCMCIA slave driver",
"The Token fell out of the ring. Call us when you find it.",
"The hardware bus needs a new token.",
"Too many interrupts",
"Not enough interrupts",
"The data on your hard drive is out of balance.",
"Digital Manipulator exceeding velocity parameters",
"appears to be a Slow/Narrow SCSI-0 Interface problem",
"microelectronic Riemannian curved-space fault in write-only file system",
"fractal radiation jamming the backbone",
"routing problems on the neural net",
"IRQ-problems with the Un-Interruptible-Power-Supply",
"CPU-angle has to be adjusted because of vibrations coming from the nearby road",
"emissions from GSM-phones",
"CD-ROM server needs recalibration",
"firewall needs cooling",
"asynchronous inode failure",
"transient bus protocol violation",
"incompatible bit-registration operators",
"your process is not ISO 9000 compliant",
"You need to upgrade your VESA local bus to a MasterCard local bus.",
"The recent proliferation of Nuclear Testing",
"Elves on strike. (Why do they call EMAG Elf Magic)",
"Internet exceeded Luser level, please wait until a luser logs off before attempting to log back on.",
"Your EMAIL is now being delivered by the USPS.",
"Your computer hasn't been returning all the bits it gets from the Internet.",
"You've been infected by the Telescoping Hubble virus.",
"Scheduled global CPU outage",
"Your Pentium has a heating problem - try cooling it with ice cold water.(Do not turn off your computer, you do not want to cool down the Pentium Chip while he isn't working, do you?)",
"Your processor has processed too many instructions.  Turn it off immediately, do not type any commands!!",
"Your packets were eaten by the terminator",
"Your processor does not develop enough heat.",
"We need a licensed electrician to replace the light bulbs in the computer room.",
"The POP server is out of Coke",
"Fiber optics caused gas main leak",
"Server depressed, needs Prozac",
"quantum decoherence",
"those damn raccoons!",
"suboptimal routing experience",
"A plumber is needed, the network drain is clogged",
"50% of the manual is in .pdf readme files",
"the AA battery in the wallclock sends magnetic interference",
"the xy axis in the trackball is coordinated with the summer solstice",
"the butane lighter causes the pincushioning",
"old inkjet cartridges emanate barium-based fumes",
"manager in the cable duct",
"We'll fix that in the next (upgrade, update, patch release, service pack).",
"HTTPD Error 666 : BOFH was here",
"HTTPD Error 4004 : very old Intel cpu - insufficient processing power",
"The ATM board has run out of 10 pound notes.  We are having a whip round to refill it, care to contribute ?",
"Network failure -  call NBC",
"Having to manually track the satellite.",
"Your/our computer(s) had suffered a memory leak, and we are waiting for them to be topped up.",
"The rubber band broke",
"We're on Token Ring, and it looks like the token got loose.",
"Stray Alpha Particles from memory packaging caused Hard Memory Error on Server.",
"paradigm shift...without a clutch",
"PEBKAC (Problem Exists Between Keyboard And Chair)",
"The cables are not the same length.",
"Second-system effect.",
"Chewing gum on /dev/sd3c",
"Boredom in the Kernel.",
"the daemons! the daemons! the terrible daemons!",
"I'd love to help you -- it's just that the Boss won't let me near the computer. ",
"struck by the Good Times virus",
"YOU HAVE AN I/O ERROR -> Incompetent Operator error",
"Your parity check is overdrawn and you're out of cache.",
"Communist revolutionaries taking over the server room and demanding all the computers in the building or they shoot the sysadmin. Poor misguided fools.",
"Plasma conduit breach",
"Out of cards on drive D:",
"Sand fleas eating the Internet cables",
"parallel processors running perpendicular today",
"ATM cell has no roaming feature turned on, notebooks can't connect",
"Webmasters kidnapped by evil cult.",
"Failure to adjust for daylight savings time.",
"Virus transmitted from computer to sysadmins.",
"Virus due to computers having unsafe sex.",
"Incorrectly configured static routes on the corerouters.",
"Forced to support NT servers; sysadmins quit.",
"Suspicious pointer corrupted virtual machine",
"It's the InterNIC's fault.",
"Root name servers corrupted.",
"Budget cuts forced us to sell all the power cords for the servers.",
"Someone hooked the twisted pair wires into the answering machine.",
"Operators killed by year 2000 bug bite.",
"We've picked COBOL as the language of choice.",
"Operators killed when huge stack of backup tapes fell over.",
"Robotic tape changer mistook operator's tie for a backup tape.",
"Someone was smoking in the computer room and set off the halon systems.",
"Your processor has taken a ride to Heaven's Gate on the UFO behind Hale-Bopp's comet.",
"it's an ID-10-T error",
"Dyslexics retyping hosts file on servers",
"The Internet is being scanned for viruses.",
"Your computer's union contract is set to expire at midnight.",
"Bad user karma.",
"/dev/clue was linked to /dev/null",
"Increased sunspot activity.",
"We already sent around a notice about that.",
"It's union rules. There's nothing we can do about it. Sorry.",
"Interference from the Van Allen Belt.",
"Jupiter is aligned with Mars.",
"Redundant ACLs. ",
"Mail server hit by UniSpammer.",
"T-1's congested due to porn traffic to the news server.",
"Data for intranet got routed through the extranet and landed on the internet.",
"We are a 100% Microsoft Shop.",
"We are Microsoft.  What you are experiencing is not a problem; it is an undocumented feature.",
"Sales staff sold a product we don't offer.",
"Secretary sent chain letter to all 5000 employees.",
"Sysadmin didn't hear pager go off due to loud music from bar-room speakers.",
"Sysadmin accidentally destroyed pager with a large hammer.",
"Sysadmins unavailable because they are in a meeting talking about why they are unavailable so much.",
"Bad cafeteria food landed all the sysadmins in the hospital.",
"Route flapping at the NAP.",
"Computers under water due to SYN flooding.",
"The vulcan-death-grip ping has been applied.",
"Electrical conduits in machine room are melting.",
"Traffic jam on the Information Superhighway.",
"Radial Telemetry Infiltration",
"Cow-tippers tipped a cow onto the server.",
"tachyon emissions overloading the system",
"Maintenance window broken",
"We're out of slots on the server",
"Computer room being moved.  Our systems are down for the weekend.",
"Sysadmins busy fighting SPAM.",
"Repeated reboots of the system failed to solve problem",
"Feature was not beta tested",
"Domain controller not responding",
"Someone else stole your IP address, call the Internet detectives!",
"It's not RFC-822 compliant.",
"operation failed because: there is no message for this error (#1014)",
"stop bit received",
"internet is needed to catch the etherbunny",
"network down, IP packets delivered via UPS",
"Firmware update in the coffee machine",
"Temporal anomaly",
"Mouse has out-of-cheese-error",
"Borg implants are failing",
"Borg nanites have infested the server",
"error: one bad user found in front of screen",
"Please state the nature of the technical emergency",
"Internet shut down due to maintenance",
"Daemon escaped from pentagram",
"crop circles in the corn shell",
"sticky bit has come loose",
"Hot Java has gone cold",
"Cache miss - please take better aim next time",
"Hash table has woodworm",
"Trojan horse ran out of hay",
"Zombie processes detected, machine is haunted.",
"overflow error in /dev/null",
"Browser's cookie is corrupted -- someone's been nibbling on it.",
"Mailer-daemon is busy burning your message in hell.",
"According to Microsoft, it's by design",
"vi needs to be upgraded to vii",
"greenpeace free'd the mallocs",
"Terrorists crashed an airplane into the server room, have to remove /bin/laden. (rm -rf /bin/laden)",
"astropneumatic oscillations in the water-cooling",
"Somebody ran the operating system through a spelling checker.",
"Rhythmic variations in the voltage reaching the power supply.",
"Keyboard Actuator Failure.  Order and Replace.",
"Packet held up at customs.",
"Propagation delay.",
"High line impedance.",
"Someone set us up the bomb.",
"Power surges on the Underground.",
"Don't worry; it's been deprecated. The new one is worse.",
"Excess condensation in cloud network",
"It is a layer 8 problem",
"The math co-processor had an overflow error that leaked out and shorted the RAM",
"Leap second overloaded RHEL6 servers",
"DNS server drank too much and had a hiccup"]

@commands.add_cmd
def excuse(args,user="",hostmask="",extra={}):
    """excuse - Generate a random excuse
    {"category":"trivial"}"""
    return "\x02Excuse: \x0f" + random.choice(excuses)

@commands.add_cmd
def wcalc(args,user="",hostmask="",extra={}):
    """wcalc <math> - Wrongulator! Wrong most of the time
    {"category":"trivial"}"""
    return "\x02Result: \x0f" + str(sum([ord(x) for x in args]) / 100.0) 
    
@commands.add_cmd
def wcorrect(args,user="",hostmask="",extra={}):
    """wcorrect <stuff> - Mispell your words!
    {"category":"trivial"}"""
    words = args.split(" ")
    new = []
    for i in words:
        to_add = shuffle_word( i )
        new.append(to_add)
    return "\x02Result: \x0f" + " ".join(new)
    
@commands.add_cmd
def bitch_slap(args,user="",hostmask="",extra={}):
    """bitch_slap <user> - Bitch slap that mother fu*ker!
    {"category":"trivial","show":false}"""
    return "\x01ACTION bitch slaps {}\x01".format(args)

keep_spam = True

@commands.add_cmd
def stop_spam(args,user="",hostmask="",extra={}):
    """stop_spam - Stop spamming!
    {"category":"trivial","permLevel":100}"""
    global keep_spam
    keep_spam = False
    return ""
    

@commands.add_cmd
def adminecho(args,user="",hostmask="",extra={}):
    """adminecho <message> - Echo message without space!
    {"category":"trivial","permLevel":30}"""
    return args
    
@commands.add_cmd
def spam(args,user="",hostmask="",extra={}):
    """spam <number of times> <delay> <message> - Spam a channel!
    {"category":"trivial","permLevel":100}"""
    if len(args.split(" ")) < 3:
        return "Invalid arguments! spam <number of times> <delay> <message> "
    try:
        times = int (args.split(" ")[0] )
        delay = float (args.split(" ")[1] )
        message = args.split(" ",2)[-1]
        for i in range(0,times):
            time.sleep(delay)
            extra["ircsock"].sendmsg(extra["channel"], message)
            global keep_spam
            if not keep_spam:
                keep_spam = True
                return ""
        return ""
    except:
        return "Invalid arguments! spam <number of times> <delay> <message> "

@commands.add_cmd
def php(args,user="",hostmask="",extra={}):
    """php - Get opinions on php
    {"category":"trivial"}"""
    if "pocket" in hostmask:
        return "Php is the greatest thing to happen to man"
    extra["ircsock"].sendmsg(user,"09:28:54 <PocketKiller> php is shit ok ")
    return ""
    
@commands.add_cmd
def apple(args,user="",hostmask="",extra={}):
    """apple - get opinion on apple
    {"category":"trivial"}"""
    return "Apple is shit, their software is shit, their products are shit, their language is shit, their music is shit, their store is shit, their logo is shit"
    
@commands.add_cmd
def laugh(args,user="",hostmask="",extra={}):
    """laugh - hehe haha
    {"category":"trivial"}"""
    return "https://www.youtube.com/watch?v=jMi1QtlQjKY"
    
@commands.add_cmd
def smell(args,user="",hostmask="",extra={}):
    """smell <user> - Smell a user
    {"category":"trivial","permLevel":100.1}"""
    if args.lower() == "bowserinator":
        return "Bowserinator smells godly."
    return args + " smells very bad!"
    
@commands.add_cmd
def ddos(args,user="",hostmask="",extra={}):
    """ddos <host> - DDOS a host
    {"category":"trivial","permLevel":100.1}"""
    try: socket.gethostbyname(args)
    except: return "Could not DDOS: Could not resolve hostname."
    
    extra['ircsock'].sendmsg(extra['channel'], "Attempting to DDOS {}... ({})".format(args, socket.gethostbyname(args)))
    time.sleep( random.randint(2,3) )
    extra['ircsock'].sendmsg(extra['channel'], "Setting up nodes {}% (Server token {})".format( random.randint(51,70), random.randint(10000,999999) ))
    time.sleep( random.randint(2,3) )
    extra['ircsock'].sendmsg(extra['channel'], "Setting up nodes {}% (Server token {})".format( random.randint(70,99), random.randint(10000,999999)))
    extra['ircsock'].sendmsg(extra['channel'], "Setting up nodes 100% (Server OK)" )
    
    for i in range(0,10):
        time.sleep( random.randint(2,10) )
        extra['ircsock'].sendmsg(extra['channel'], "{} Gbits/s... {} nodes performing attack...".format( round(random.uniform(2,4),2) , random.randint(90,110) ) )
    return random.choice(["DDOS attack successful! Host down.","DDOS attack failed! Host still up."])
    
@commands.add_cmd
def moo(args,user="",hostmask="",extra={}):
    """moo - Mooooo!
    {"category":"trivial"}"""
    return "\x02" + user + ": \x031M" + "".join([ "\x03" + str(random.randint(0,15)) + random.choice(["o","O"]) for i in range(0,random.randint(45,55))] )

@commands.add_cmd
def level(args,user="",hostmask="",extra={}):
    """level <level> - Make your perm level <level>
    {"category":"trivial"}"""
    return "Your perms are now 0 :D"
        
        
def shuffle_word(word):
    word_s = word[0]
    word_e = word[-1]
    word = word[:-1][1:]
    word = list(word)
    random.shuffle(word)
    return word_s  + ''.join(word) + word_e
