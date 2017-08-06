import traceback, time, os, sys, threading
import datetime, Queue
import select, gc
import datetime
import commands, IO, misc

from Trival import ctcp

commands.ircsock.changenick( commands.nick )
ircsock = commands.ircsock
ircsock.sendmsg("NickServ","identify {0}".format(commands.password))

verbs = open('Trival/verbs.txt','r').read().split("\n")

#Other variables for input and such
inputQueue = []
outputQueue = [] #USED ONLY BY NORMAL COMMANDS, SOME DIRECTLY USE IRCSOCKET

queue = Queue.Queue()

print "Connecting done."

while 1:
    try: 
        #THIS IS TO FIX WEIRD THREADING BUG :P
        ready = select.select([commands.ircsock.ircsock], [], [], 0.0)
        messages = []
        if ready[0]: 
            messages = commands.ircsock.ircsock.recv(2048).replace("\r","").split("\n")
        inputQueue.append( IO.Input("A!B@h PRIVMSG #s :NOPRINT") ) #
        
        for m in messages:
            try: 
                if(m != None and m != ""):
                    inputQueue.append( IO.Input(m) ) #Add messages to input queue
            
            except IndexError: 
                commands.log.info("Disconnected from IRC server, attempting to restart bot...")
                time.sleep(1)
                os.execv(sys.executable, [sys.executable] + sys.argv) 
        
        while len(inputQueue) > 0: #Continue if there are still more input
            ircmsg = inputQueue[0]
            if ircmsg.message != "NOPRINT":
                commands.log.recv( ircmsg.raw )
            
                            
            commands.update_bombs(ircsock) #Update time bombs
                
            #Server reconnecting
            if ircmsg.type == None:
                pass
                #commands.log.info("Disconnected from IRC server, attempting to restart bot...")
                #time.sleep(5)
                #os.execv(sys.executable, [sys.executable] + sys.argv) 
            elif ircmsg.type == "432":
                commands.log.error("Erroneous Nickname, using fallback nick")
                #Actually quit for insomnia cronjob
                sys.exit(0)
                #ircsock.changenick( commands.nick2 )
            elif ircmsg.type == "433":
                commands.log.error("Nickname in use, using fallback nick")
                #Actually quit for insomnia cronjob
                sys.exit(0)
                #ircsock.changenick( commands.nick2 )
            elif ircmsg.type == "376": #Add space between MOTD and bot stuff
                commands.ircsock.joinchan( ",".join(commands.channels) )
                print(" ")
                
                
            elif ircmsg.type == "INVITE":
                if ircmsg.channel.lower() not in commands.blacklistchan:
                    ircsock.joinchan(ircmsg.channel)
            
            
            #PRIVATE MESSAGE HANDLER
            elif ircmsg.type == "PRIVMSG":
                channel = ircmsg.channel
                message = ircmsg.message
                user = ircmsg.user.split("!")[0].replace(":","",1)
                hostmask = ircmsg.user.split("@",1)[1]
                
                if user == "jeffl35-mc":
                    try: message = message.split("> ")[1]
                    except: pass

                commands.update_reminders(user,channel,message,ircsock)
                
                if commands.enablePM: #Handle private messages
                    if channel == commands.nick:
                        channel = user
                        
                if ircmsg.channel.lower() == commands.nick.lower(): #Handle CTCP
                    result = ctcp.runctcp( ircmsg, commands )
                    if result:
                        ircsock.notice( user, result )
                
                extra = { "channel": channel, "config":commands, "output":outputQueue, "ircsock":ircsock, "ircmsg":ircmsg }
                t1 = threading.Thread(target=misc.doCheck, args=(channel, message, user, hostmask, extra))
                t1.setDaemon(True); 
                t1.start(); 
                
                if commands.userPerms.get(hostmask,0) >= 100 and message.split(" ")[0] == commands.commandChar + "r":
                    commands.commands = []
                    commands.r()
                    reload(misc)
                    ircsock.sendmsg(channel, "Reload successful!")
                
                doneCommand = False
                for command in commands.commands:
                    
                    #Check for the command in the message
                    if commands.unsafeCommandChar:
                        doCommand = (commands.commandChar + command.name) in message
                        if doCommand:
                            try: args = message.split(commands.commandChar+command.name+ " ",1)[1]
                            except: args = ""
                        if doCommand == False:
                            for c in command.alias:
                                if (commands.commandChar + c) in message:
                                    doCommand = True
                                    try: args = message.split(commands.commandChar+c+ " ",1)[1]
                                    except: args = ""
                    else:
                        doCommand = message.split(" ")[0] == commands.commandChar + command.name
                        if doCommand:
                            try: args = message.split(commands.commandChar+command.name+ " ",1)[1]
                            except: args = ""
                        if doCommand == False:
                            for c in command.alias:
                                if message.split(" ")[0] == commands.commandChar + c:
                                    doCommand = True
                                    try: args = message.split(commands.commandChar+c+ " ",1)[1]
                                    except: args = ""
                    
                        
                    #Run the command
                    if doCommand:
                        doneCommand = True
                        if commands.userPerms.get(hostmask,0) >= command.permLevel:
                            try: args
                            except: args = ""
                            
                            if command.threaded:
                                t1 = threading.Thread(target=commands.runCommand, args=(args, hostmask, user, extra, command, queue, channel))
                                t1.setDaemon(True); 
                                t1.start(); 
                            else:
                                outputQueue.append( [channel, command.function( args, user, hostmask, extra ) ] )
                        elif command.exist:
                            if user != "handicraftsman":
                                outputQueue.append( [channel, "You do not have permission to use this command (lvl {})".format(command.permLevel)] )
                
                if not doneCommand:
                    for v in verbs:
                        if message.split(" ")[0] == (commands.commandChar + v):
                            try: args = message.split(commands.commandChar+v+ " ",1)[1]
                            except: args = ""
                            outputQueue.append( [channel, "\x01ACTION {}s {}\x01".format(v,args) ] )

                    
            while queue.qsize():
                outputQueue.append( queue.get() )
                
            if commands.userPerms.get(hostmask,0) >= 100 and message.split(" ")[0] == commands.commandChar + "flushq":
                outputQueue = []
                ircsock.sendmsg(channel, "OutputQueue flushed!")
                    
            #AUTO REJOIN CHANNELS
            #for channel in commands.channels:
            if ircmsg.type == "KICK" and ircmsg.userkicked.lower() == commands.nick.lower():# and ircmsg.channel.lower() == channel.lower():
                ircsock.joinchan(ircmsg.channel)
                time.sleep(1)
                ircsock.joinchan(ircmsg.channel)
            if ircmsg.type == "PART" and commands.nick.lower() in ircmsg.user.lower() and "requested by" in ircmsg.raw.lower():
                ircsock.joinchan(ircmsg.channel)
                time.sleep(1)
                ircsock.joinchan(ircmsg.channel)
                time.sleep(2)
                
                if commands.nick.lower() not in ircmsg.raw.split("requested by ")[1].split(" ")[0].lower():
                    ircsock.remove(ircmsg.channel, ircmsg.raw.split("requested by ")[1].split(" ")[0], "Fuck off")
            if ircmsg.type == "PART" and "bowserinator" in ircmsg.user.lower() and "requested by" in ircmsg.raw.lower():
                if commands.nick.lower() not in ircmsg.raw.split("requested by ")[1].split(" ")[0].lower():
                    ircsock.remove(ircmsg.channel, ircmsg.raw.split("requested by ")[1].split(" ")[0], "Fuck off")
                    
            

            #PING
            if ircmsg.type == "PING":
                commands.ircsock.ping()

            del inputQueue[0] #Remove that from the list

        #SEND UR SHIT :)
        for x in range(0,len(outputQueue)):
            n = 340; msg=str( outputQueue[x][1] )
            msg = [msg[i:i+n] for i in range(0, len(msg), n)]
            chan = outputQueue[x][0]
            
            #CAPS LOCK DAY :) :) :)
            if datetime.datetime.now().day == 22 and datetime.datetime.now().month == 10:
                m = m.upper()
            elif datetime.datetime.now().day == 28 and datetime.datetime.now().month == 6:
                m = m.upper()
            
            for m in msg:
                print ("[SEND] [{0}]: [{1}] {2}".format(datetime.datetime.now(),chan,m))
                ircsock.sendmsg( chan, m.replace("\n","").replace("\r","").replace("\t","") )
                time.sleep(0.5)
            del outputQueue[x]
    
    except KeyboardInterrupt: 
        pass
    except: 
        traceback.print_exc()    #Print the error if something goes wrong
        outputQueue = []
        inputQueue = []

    time.sleep(0.2) #To avoid 100% CPU usage :(
    gc.collect() #Free memory