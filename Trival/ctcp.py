#FINGER USERINFO SOURCE FINGER CLIENTINFO
import time, datetime

def runctcp( ircmsg, commands ):
    if "PING" in ircmsg.message:
        return  "{}".format( ircmsg.message.replace("\n","").replace("\r","")  )
    elif "TIME" in ircmsg.message:
        return "{}".format( datetime.datetime.now().strftime("%Y-%m-%d %H:%M") )
    elif "VERSION" in ircmsg.message:
        return "VERSION HexChat 2.9.1 [x86] / Windows 8 [1.46GHz]"
    elif "FINGER" in ircmsg.message:
        return "Firstname Lastname"
    elif "SOURCE" in ircmsg.message:
        return "Source not avaliable."
    elif "USERINFO" in ircmsg.message:
        return "I'm just your typical IRC user, you know."
    elif "ERRMSG" in ircmsg.message:
        return "ERROR! ERROR! ERROR!"
    return "Default CTCP reply! :)"