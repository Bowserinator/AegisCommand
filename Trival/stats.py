"""Generate Stats For the Bot

Stats Include:
    > Most used commands
    > Messages seen
    > Number of pings
    > Number of commands
    > Reloads"""
import json, time

try: data = json.loads( open("Trival/stats.json","r").read() )
except: data = {}
if data == {}:
    data = {
        "reload":0,
        "ping":0,
        "commands":0,
        "seen":0,
        "commands2": {
            
        }
    }

def parse( ircmsg, commands ):
    file = open("Trival/stats.json", "w")
    file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')) )
    file.close()

    if ircmsg.type == "PING":
        data["ping"] += 1
        
    if ircmsg.type == "PRIVMSG":
        if ircmsg.message == commands.commandChar + "r":
            data["reload"] += 1
        elif ircmsg.message.startswith(commands.commandChar):
            data["commands"] += 1
            
            if ircmsg.message.split(" ")[0].replace(commands.commandChar, "") in [c.name for c in commands.commands]:
                try: data["commands2"][ircmsg.message.split(" ")[0].replace(commands.commandChar, "").lower()] += 1
                except: data["commands2"][ircmsg.message.split(" ")[0].replace(commands.commandChar, "").lower()] = 1
        data["seen"] += 1
    