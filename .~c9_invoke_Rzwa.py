import traceback, time, os, sys, threading
import datetime

import commands, IO

commands.ircsock.changenick( commands.nick )
commands.ircsock.joinchan( ",".join(commands.channels) )
ircsock = commands.ircsock

#Other variables for input and such
inputQueue = []
outputQueue = [] #USED ONLY BY NORMAL COMMANDS, SOME DIRECTLY USE IRCSOCKET


while 1:
    try: 
        messages = commands.ircsock.ircsock.recv(2048).replace("\r","").split("\n")
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
            commands.log.recv( ircmsg.raw )
            
            #Server reconnecting
            if ircmsg.type == None:
                commands.log.info("Disconnected from IRC server, attempting to restart bot...")
                time.sleep(1)
                os.execv(sys.executable, [sys.executable] + sys.argv) 
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
                print(" ")
                
                
            
            #PRIVATE MESSAGE HANDLER
            elif ircmsg.type == "PRIVMSG":
                channel = ircmsg.channel
                message = ircmsg.message
                user = ircmsg.user.split("!")[0]
                hostmask = ircmsg.user.split("@",1)[1]
                
                if message.split(" ")[0].startswith(commands.commandChar + "r"):
                    commands.commands = []
                    commands.r()
                    ircsock.sendmsg(channel, "Reload successful!")
                
                for command in commands.commands:
                    if message.split(" ")[0] == commands.commandChar + command.name:
                        if commands.userPerms.get(hostmask,0) >= command.permLevel:
                            #TEMP
                            try: args = message.split(commands.commandChar+command.name+ " ",1)[1]
                            except: args = ""
                            
                            outputQueue.append( [channel, command.function( args, hostmask, user ) ] )
                            
                            #ircsock.sendmsg(channel, command.function( args, hostmask, user ) )
                        else:
                            outputQueue.append( [channel, "You do not have permission to use this command (lvl {})".format(command.permLevel)] )
                    
                    
            #AUTO REJOIN CHANNELS
            for channel in commands.channels:
                if ircmsg.type == "KICK" and ircmsg.userkicked.lower() == commands.nick.lower() and ircmsg.channel.lower() == channel.lower():
                    ircsock.joinchan(channel)
                    time.sleep(1)
                    ircsock.joinchan(channel)
                if ircmsg.type == "PART" and commands.nick.lower() in ircmsg.user.lower() and "requested by" in ircmsg.raw.lower():
                    ircsock.joinchan(channel)
                    time.sleep(1)
                    ircsock.joinchan(channel)
                    
            

            #PING
            if ircmsg.type == "PING":
                commands.ircsock.ping()
                
            del inputQueue[0] #Remove that from the list

        #SEND UR SHIT :)
        for x in range(0,len(outputQueue)):
            n = 340; msg=str( outputQueue[x][1] )
            msg = [msg[i:i+n] for i in range(0, len(msg), n)]
            chan = outputQueue[x][0]
            
            for m in msg:
                print ("[SEND] [{0}]: [{1}] {2}".format(datetime.datetime.now(),chan,m))
                ircsock.sendmsg( chan, m )
                time.sleep(0.5)
            del outputQueue[x]
    
    except KeyboardInterrupt: 
        pass
    except: 
        traceback.print_exc()    #Print the error if something goes wrong
