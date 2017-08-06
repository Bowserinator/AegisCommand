#enchant possible, enchant prob, enchant best slot, enchant best, craftcalc, toolstats, craft, search, 
# mcwiki, brew, mcuserstats, mcstatus, gettile, getnearest
import dynmap, web, re, brewing, enchant, crafting
web = web.Web()
dynmap = dynmap.dynmap
brew = brewing.brew()

import json
recipies_raw = open("MC/recipies.txt", "r").read()
recipies = json.loads(recipies_raw)


import sys, time
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import commands



@commands.add_cmd
def enchant_possible(args="",user=None,hostmask=None,extra={}): 
    """enchant_possible [item],[slot],[book shelves] - Get possible enchants for tool
    {"category":"mc","permLevel":50}"""
    try:
        returned = ""
        y = args.split(",")
        for e in enchant.getPossibleEnchants(y[0],int(y[1]),int(y[2])): #Possible enchants at slot
            returned = returned + e.name + " " + str(e.level) + " | "
        return "\x02Possible enchants: \x0f" + returned
    except:
        return "Invalid arguments found. Format is enchant_possible [item],[slot],[book shelves]"
        
@commands.add_cmd
def enchant_prob(args="",user=None,hostmask=None,extra={}): 
    """enchant_prob [enchant],[item],[slot],[books] - Get prob of getting enchant
    {"category":"mc","permLevel":50}"""
    try:
        y = args.split(",")
        prob = enchant.getProbEnchant(y[0],y[1],int(y[2]),int(y[3]))
        return str(prob * 100) + "% chance of getting " + y[0] + " on slot " + y[2] + " with " + y[3] + " books."
    except Exception as e:
        return "\x034" +"Invalid Input, use format enchant prob [enchant],[item],[slot],[books]."

@commands.add_cmd
def enchant_best_slot(args="",user=None,hostmask=None,extra={}): 
    """enchant_best_slot [enchant],[item],[books] - Get best slot to get enchant
    {"category":"mc","permLevel":50}"""
    try:
        y = args.split(",")
        slot = enchant.getBestSlot(y[0],y[1],int(y[2]))
        slots = ["Top","Middle","Bottom"]
        return slots[slot[0]-1] + " is the best slot with " + str(slot[1]*100) + "% chance."
    except Exception as e:
        return "\x034" +"Invalid Input, use format enchant best_slot [enchant],[item],[books] ."

@commands.add_cmd
def enchant_best(args="",user=None,hostmask=None,extra={}): 
    """enchant_best [enchant],[item] - Best way to get enchant on item
    {"category":"mc","permLevel":50}"""
    try:
        y = args.split(",")
        slot = enchant.getBestLevel(y[0],y[1])
        
        slots = ["Top","Middle","Bottom"]
        return slots[slot[1]-1] + " slot with " + str(slot[0]) + " books yeilds " + str(slot[2]*100) + "% chance."
    except Exception as e:
        return "\x034" +"Invalid Input, use format enchant_best [enchant],[item] ."


@commands.add_cmd
def craftcalc(args="",user=None,hostmask=None,extra={}): 
    """craftcalc [item] [amount] - Calculate resources to craft [amount] items
    {"category":"mc"}"""
    try:
        y = args.split(" ")
        y[0] = y[0].lower()
        slot = crafting.RecipieCalc(y[0],recipies, int(y[1]))

        return "\x02Resources: \x0f" + slot
    except Exception as e:
        return "\x034" +"Invalid Input, use format craftcalc [item],[amount] ."
            
@commands.add_cmd
def craft(args="",user=None,hostmask=None,extra={}): 
    """craft [item] - Craft an item
    {"category":"mc"}"""
    try:
        a = args
        r = crafting.getRecipieStr(a,recipies)
        extra['ircsock'].sendmsg(extra['channel'], r[0])
        extra['ircsock'].sendmsg(extra['channel'], r[1])
        return r[2]
    except Exception as e:
        return "\x034" +"Recipe not found, try search"
            
@commands.add_cmd
def search(args="",user=None,hostmask=None,extra={}): 
    """search [item] - Search for name of item
    {"category":"mc"}"""
    try:
        a = args
        r = crafting.searchRecipie(a,recipies)
        if r.replace(" ","") == "":
            return "No matches found."
        return r
    except Exception as e:
        return "No matches found.."


@commands.add_cmd
def get_time(args="",user=None,hostmask=None,extra={}): 
    """get_time - Get server time
    {"category":"mc","alias":["gettime"]}"""
    dynmap.update()
    returned = dynmap.getServerTime()["time"] 
    if dynmap.getServerTime()["canSleep"]: returned = returned + " (You can sleep)"
    return "\x02Server Time: \x0f" + returned

@commands.add_cmd
def get_tick(args="",user=None,hostmask=None,extra={}): 
    """get_tick - Get raw server time
    {"category":"mc","alias":["gettick"]}"""
    dynmap.update()
    returned = dynmap.getServerTick()
    return "\x02Server Tick: \x0f" + str(returned)

@commands.add_cmd
def get_player(args="",user=None,hostmask=None,extra={}): 
    """get_player <nick> - Get data for player
    {"category":"mc","alias":["getplayer"]}"""
    dynmap.update()
    players = dynmap.getPlayers()
    try: 
        data = dynmap.getPlayerData(args)
        data["x"] = round(data["x"],2)
        data["y"] = round(data["y"],2)
        data["z"] = round(data["z"],2)
        returned = data["name"] + " is at " + "{0},{1},{2}".format(data["x"],data["y"],data["z"]) 
        world = {"world":"overworld","world_nether":"nether","world_the_end":"end"}[data["world"]]
        returned = returned + " in the {0} and has {1} health and {2} armour.".format(world,data["health"],data["armor"])
        return returned
    except: return "Could not find user, possibly hidden on dynmap?"

@commands.add_cmd
def get_weather(args="",user=None,hostmask=None,extra={}): 
    """get_weather - Get weather
    {"category":"mc","alias":["getweather"]}"""
    dynmap.update()
    return "\x02Weather:\x0f Thundering: {0} | Raining: {1}".format(dynmap.isThundering(), dynmap.hasStorm())

@commands.add_cmd
def online(args="",user=None,hostmask=None,extra={}): 
    """online - Get online users
    {"category":"mc"}"""
    dynmap.update()
    names = [x["name"] for x in dynmap.getPlayers()]
    if len(names) == 0: return "There are no players online on dynmap right now."
    return "\x02Online:\x0f " + " ".join(names)

@commands.add_cmd
def get_map(args="",user=None,hostmask=None,extra={}): 
    """get_map <x,y,z> <overworld/nether/end> <flat/3d/cave> - Get url for map at location
    {"category":"mc","alias":["getmap"]}"""
    world = "overworld" 
    view = "flat"
    worlds = {"overworld":"world","nether":"world_nether","end":"world_the_end"}
    views = {"flat":"flat","3d":"surface","cave":"cave"}
    args = args.lower()
    
    if "overworld" in args:
        args = args.strip('nether').strip('overworld')
    elif "nether" in args or "hell" in args:
        world = "nether"
        args = args.strip('nether').strip('hell')
    elif "end" in args:
        world = "end"
        args = args.strip('end')
    
    if "flat" in args: args = args.strip('flat')
    elif "3d" in args: args = args.strip('3d'); view = "3d"
    elif "cave" in args: args = args.strip('cave'); view = "cave"
        
    args = args.lstrip().rstrip()
    world = worlds[world]
    view = views[view]
    dynmap.update()
    
    try: #Get the location of [player name] and return world
        if dynmap.getPlayerData(args): #If it's a valid player return map
            data = dynmap.getPlayerData(args)
            url = "http://dynmap.starcatcher.us/?worldname={0}&mapname={1}&zoom=6&x={2}&y={3}&z={4}".format(data["world"],view,data["x"],data["y"],data["z"])
            try: return web.isgd(url)
            except: return url
    except: pass

    #Obtain the location of [location] and return map
    locations = {
        "azure":{"cord":[-69,-220], "world":"world"},
        "spawn":{"cord":[-211,142], "world":"world"},
        "end portal":{"cord":[-115,-126], "world":"world_nether"},
    }
    
    for key in locations:
        if key in args.lower():
            url = "http://dynmap.starcatcher.us/?worldname={0}&mapname={1}&zoom=6&x={2}&y={3}&z={4}".format(locations[key]["world"],view,locations[key]["cord"][0],65,locations[key]["cord"][1])
            try: return web.isgd(url)
            except: return url
            
    #Obtain coordinates
    cords = re.findall("([-+]?)([:]?\d*\.\d+|\d+),([-+]?)([:]?\d*\.\d+|\d+),([-+]?)([:]?\d*\.\d+|\d+)",args.replace(" ",""))
    if cords == []: cords = re.findall("([-+]?)([:]?\d*\.\d+|\d+),([-+]?)([:]?\d*\.\d+|\d+)",args.replace(" ",""))
    cords2 = []
    for i in cords[0]: cords2.append(i)
    x = cords2[0] + cords2[1]
    if len(cords2) == 4: 
        y = "65"; z = cords2[2]+cords2[3]
    elif len(cords2) == 6: 
        y = cords2[2]+cords2[3]
        z = cords2[4]+cords2[5]
    url = "http://dynmap.starcatcher.us/?worldname={0}&mapname={1}&zoom=6&x={2}&y={3}&z={4}".format(world,view,x,y,z)
    try: return web.isgd(url)
    except: return url

@commands.add_cmd
def getclaim(args="",user=None,hostmask=None,extra={}): 
    """getclaim <user> - Get claim user is in
    {"category":"mc","alias":["get_claim"]}"""
    dynmap.update()
    try:
        player = dynmap.getPlayerData(args)
        x = player["x"]; z = player["z"]
        claims = dynmap.getClaims()
        for key in claims:
            claim2 = claims[key]
            if type(claim2) == dict: claim = claim2
            else: claim = claim2[0]
    
            if isBetween(x,z,claim['corners'][0], claim['corners'][1], claim['corners'][2], claim['corners'][3]):
                return "{0} is currently in a {1}x{2} ({3}) claim by {4}. \x02Permission trust:\x0f {5} | \x02Build:\x0f {6} | \x02Container:\x0f {7}".format(
                    player["name"],
                    int(abs(claim["corners"][0] - claim["corners"][2])),
                    int(abs(claim["corners"][1] - claim["corners"][3])),
                    int(abs(claim["corners"][0] - claim["corners"][2]) * abs(claim["corners"][1] - claim["corners"][3])),
                    key.split("_")[0],
                    ", ".join(claim["permTrust"]),
                    ", ".join(claim["trust"]),
                    ", ".join(claim["containerTrust"]),
                )
        return "{0} is currently not standing inside a claim.".format(player["name"])
    except: return "Could not find player {0}.".format(args)
    
def isBetween(x,z,x1,z1,x2,z2):
    if (x>x1 and x<x2) or (x>x2 and x<x1):
        if (z>z1 and z<z2) or (z>z2 and z<z1):
            return True
    return False

@commands.add_cmd
def getowc(args="",user=None,hostmask=None,extra={}): 
    """getowc x,y,z - Convert nether to overworld
    {"category":"mc"}"""
    cords = args.replace(","," ").split(" ")
    if len(cords) == 2:
        return "\x02Conversion: \x0f{0},{1}".format(float(cords[0])*8, float(cords[1])*8 )
    elif len(cords) == 3:
        return "\x02Conversion: \x0f{0},{1},{2}".format(float(cords[0])*8, float(cords[1]), float(cords[2])*8 )

@commands.add_cmd  
def getnwc(args="",user=None,hostmask=None,extra={}): 
    """getnwc x,y,z - Overworld to nether conversion
    {"category":"mc"}"""
    cords = args.replace(","," ").split(" ")
    if len(cords) == 2:
        return "\x02Conversion: \x0f{0},{1}".format(float(cords[0])/8, float(cords[1])/8 )
    elif len(cords) == 3:
        return "\x02Conversion: \x0f{0},{1},{2}".format(float(cords[0])/8, float(cords[1]), float(cords[2])/8 )


@commands.add_cmd  
def mcwiki(args="",user=None,hostmask=None,extra={}): 
    """mcwiki <query> - Get url for command
    {"category":"mc"}"""
    try:
        a = args.replace(" ", "+")
        return "\x02Url: \x0f\x0312" + web.tinyurl("https://minecraft.gamepedia.com/index.php?search=" + a + "&title=Special%3ASearch&go=Go")
    except:
        return "\x034" +"No search results!"
    
@commands.add_cmd  
def brew2(args="",user=None,hostmask=None,extra={}): 
    """brew <potion> - Brew a potion
    {"category":"mc","name":"brew"}"""
    try:
        query = args
        result = brew.brew(query)
        if result["possible"]:
            return "\x02Steps: \x0f" + ",".join(result["steps"]) + " \x02Time: \x0f" + str(result["time"]) + " seconds."
        else:
            return "This potion is impossible to brew in vanilla Minecraft"
    except:
        return "\x034" +"Invalid input found."