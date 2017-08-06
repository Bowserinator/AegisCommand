"""Reminder Format
{
    target: "user" who to remind
    delay: 100 time till remind
    onNextSpeech: false remind when the user next speaks
}"""

import json

import sys, time
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import commands

reminders = json.loads( open("Reminders/reminders.json","r").read() ) #Load the reminders

@commands.add_cmd
def remind(args, user="",hostmask="",extra={}):
    """remind <user> <time in seconds|talk> <message> - Remind a user, if time argument is 'talk' it will remind them when they next speak.
    {"category":"general"}"""
    global reminders
    
    try:
        if int( args.split(" ")[1] ) > 86400*2:
            return "Time difference must be less than 2 days"
    except: 
        if args.split(" ")[1] != "talk":
            return "Invalid time argument"
    
    reminders['reminders'].append( { 
        "time_posted": time.time(),
        "time_difference": str( args.split(" ")[1] ),
        "target": args.split(" ")[0],
        "message": args.split(" ",2)[-1],
        "channel": extra["channel"],
        "reminder": user
    } )
    
    
    open("Reminders/reminders.json","w").write( json.dumps(reminders, sort_keys=True, indent=4, separators=(',', ': ')) )
    return "Thanks. I will remind them."


def update_reminders(user,channel,message,irc):
    global reminders
    
    j = 0
    for i in reminders['reminders']:
        if i['time_difference'] == "talk":
            if i['channel'].lower() == channel.lower() and user.lower() == i['target'].lower():
                del reminders['reminders'][j]
                open("Reminders/reminders.json","w").write( json.dumps(reminders, sort_keys=True, indent=4, separators=(',', ': ')) )
                irc.sendmsg( channel, i['reminder'] + " reminds you: " +  i['message'] )
       
        elif time.time() - int(i['time_difference']) > i['time_posted']:
            del reminders['reminders'][j]
            open("Reminders/reminders.json","w").write( json.dumps(reminders, sort_keys=True, indent=4, separators=(',', ': ')) )
            irc.sendmsg( i['channel'], i['reminder'] + " reminds you: " + i['message'] )
        j+= 1




