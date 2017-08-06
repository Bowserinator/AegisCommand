

class brew(object):
    def __init__(self):
        pass
    
    def brew(self,pot,version=1.8): #Gets fastest way to brew a potion, along with time and fuel cost
        fuelCost = 1; time = 0
        brewArray = []
        pot = self.phraseName(pot)
        name = pot["name"]
        possible = True

        if "night vision" in name:
            brewArray = ["nether wart","golden carrot"]; time = 40
        elif "invisibility" in name:
            brewArray = ["nether wart","golden carrot","fermented spider eye"]; time = 60
        elif "leap" in name or "jump" in name:
            brewArray = ["nether wart","rabbit's foot"]; time = 40
        elif "fire resistance" in name:
            brewArray = ["nether wart","magma cream"]; time = 40
        elif "slowness" in name:
            brewArray = ["nether wart","sugar","fermented spider eye"]; time = 60
        elif "speed" in name or "swiftness" in name:
            brewArray = ["nether wart","sugar"]; time = 40
        elif "breathing" in name:
            brewArray = ["nether wart","pufferfish"]; time=40
        elif "healing" in name:
            brewArray = ["nether wart","glistering melon"]; time = 40
        elif "harming" in name:
            brewArray = ["nether wart","glistering melon","fermented spider eye"]; time = 60
        elif "poison" in name:
            brewArray = ["nether wart","spider eye"]; time = 40
        elif "regeneration" in name:
            brewArray = ["nether wart","ghast tear"]; time = 40
        elif "strength" in name:
            brewArray = ["nether wart","blaze powder"]; time = 40
        elif "weakness" in name:
            brewArray = ["nether wart","blaze powder","fermented spider eye"]; time = 60
        
        if pot["extended"]:
            brewArray.append("redstone dust"); time += 20
        if pot["level"] == 2:
            brewArray.append("glowstone dust"); time += 20
        if pot["splash"]:
            brewArray.append("gunpowder"); time += 20
        if pot["lingering"]:
            brewArray[0] = "dragon's breath"
        
        #VERIFY which ones can be possible
        if pot["level"] > 2: #No potion can have a level of over 2
            possible = False
        elif pot["level"] == 2 and pot["extended"] == True: #can't be level II and extended that the same time
            possible = False
        elif pot["splash"] and pot["lingering"]: #can't be splash and lingering at the same time
            possible = False
            
        #Potions that can't be extnended or improved
        if "weakness" in name and pot["level"] > 1: #No weakness level 2 sadly
            possible = False
        elif "slowness" in name and pot["level"] > 1: #No slowness level 2 sadly
            possible = False
        elif "fire resistance" in name and pot["level"] > 1: #No fire res level 2 sadly
            possible = False
        elif "night vision" in name and pot["level"] > 1: #No night vision level 2 sadly
            possible = False
        elif "invisibility" in name and pot["level"] > 1: #No invisible level 2 sadly
            possible = False
        elif "breathing" in name and pot["level"] > 1: #No water breathing level 2 sadly
            possible = False
        elif "healing" in name and pot["extended"]: #No healing extended
            possible = False
        elif "harming" in name and pot["extended"]: #No harming extended
            possible = False
        
            
        if version < 1.9: #No fuel cost under 1.9 lol
            fuelCost = None
        return {"name":name, "data":pot, "steps":brewArray, "possible":possible, "time":time, "fuelCost":fuelCost}
    
    def potionStats(self,pot,version=1.8): #Gets statistics on potion
        #Returns duration , description
        pot = self.brew(pot)
        possible = pot["possible"]
        data = pot["data"]
        name = pot["name"]
        level = data["level"]
        returned = ""; duration = "--:--"
        
        #FIX DURATION HERE!!!
        if "night vision" in name:
            returned = returned + "makes everything appear to be at max light level, including underwater areas."
            if pot["data"]["extended"]:
                duration = "08:00"
            else:
                duration = "03:00"
            
        elif "invisibility" in name:
            returned = returned + "Renders the player invisible. Equipped/wielded items are still visible."
            if pot["data"]["extended"]:
                duration = "08:00"
            else:
                duration = "03:00"

        elif "leap" in name or "jump" in name:
            returned = returned + "Allows the player to jump {} blocks higher and reduces fall damage by {} hearts.".format((level+4.2)**2 / 16.0, 0.5*level)
            if pot["data"]["extended"]:
                duration = "08:00"
            elif level == 2:
                duration = "01:30"
            else:
                duration = "03:00"
                
        elif "fire resistance" in name:
            returned = returned + "Gives immunity to damage from fire, lava, and ranged Blaze attacks."
            if pot["data"]["extended"]:
                duration = "08:00"
            else:
                duration = "03:00"

        elif "slowness" in name:
            returned = returned + "Contracts FOV and decreases speed to {} times normal.".format(0.85**level)
            if pot["data"]["extended"]:
                duration = "03:00"
            else:
                duration = "01:30"

        elif "speed" in name or "swiftness" in name:
            returned = returned + "Expands FOV and increases speed to {} times normal.".format(1.2**level)
            if pot["data"]["extended"]:
                duration = "08:00"
            elif level == 2:
                duration = "01:30"
            else:
                duration = "03:00"

        elif "breathing" in name:
            returned = "Does not deplete the oxygen bar when underwater."
            if pot["data"]["extended"]:
                duration = "08:00"
            else:
                duration = "03:00"

        elif "healing" in name:
            returned = "Instantly heals {} hearts.".format(2**level)

        elif "harming" in name:
            returned = "Instantly damages {} hearts.".format(1.5 * 2**level)

        elif "poison" in name:
            damageArray = {1:25 , 2:12, 3:6, 4:3, 5:1}
            try: damage = damageArray[level]
            except: damage = 1
            returned = "Does 0.5 hearts of damage every {} seconds.".format(damage/20.0)
            
            if pot["data"]["extended"]:
                duration = "02:00"
            elif level == 2:
                duration = "00:22"
            else:
                duration = "00:45"
            
        elif "regeneration" in name:
            regenArray = {1:50, 2:25, 3:12, 4:6, 5:3, 6:1}
            try: regen= regenArray[level]
            except: regen = 1
            
            returned = "Regenerates 0.5 hearts every {} seconds.".format(regen/20.0)
            if pot["data"]["extended"]:
                duration = "02:00"
            elif level == 2:
                duration = "00:22"
            else:
                duration = "00:45"

        elif "strength" in name:
            if version < 1.9:
                returned = "Does {} times more damage.".format(1.3*level)
            else:
                returned = "Does {} more hearts damage.".format(1.5*level)
            if pot["data"]["extended"]:
                duration = "08:00"
            elif level == 2:
                duration = "01:30"
            else:
                duration = "03:00"
            
        elif "weakness" in name:
            if version < 1.9:
                returned = "Decreases damage by {} hearts.".format(0.25*level)
            else:
                returned = "Decreases damage by {} hearts.".format(2*level)
            if pot["data"]["extended"]:
                duration = "08:00"
            elif level == 2:
                duration = "01:30"
            else:
                duration = "03:00"
        
        if pot["possible"] == False:
            returned = returned + " This potion cannot be brewed."
        return {"data":data,"description":returned, "duration":duration}
    
    def phraseName(self,pot): #Gets a json based on name: core potion name and level
        pot = pot.lower().replace("potion","").replace("of","").lstrip() #Delete the words potion and of and eliminate starting whitespace
        
        extended = False; splash = False; lingering = False
        if "splash" in pot:
            splash = True; pot = pot.replace("splash","")
        if "lingering" in pot:
            lingering = True; pot = pot.replace("lingering","")
        if "(extended)" in pot:
            extended = True; pot = pot.replace("(extended)","")
        if "extended" in pot:
            extended = True; pot = pot.replace("extended","")
        
        pot = pot.strip()
        level = pot.split(" ")[-1]
        
        for i in level:
            if not i.lower() in "ivxlcdm0123456789":
                pot = pot + " 1"; level = pot.split(" ")[-1]; break

        try: level = int(float(level)) #level is given as a number
        except: level = romanNumeral(level) #level is given as a roman numeral

        pot = pot.rsplit(' ', 1)[0] 
        return {"name":pot, "extended":extended, "level": level, "splash":splash, "lingering":lingering}
        
    

def romanNumeral(num): 
    #Converts romanNumerals to int
    #Credit to http://codereview.stackexchange.com/questions/5091/converting-roman-numerals-to-integers-and-vice-versa
    #For the code
    
    string = num.upper()
    table=[['M',1000],['CM',900],['D',500],['CD',400],['C',100],['XC',90],['L',50],['XL',40],['X',10],['IX',9],['V',5],['IV',4],['I',1]]
    returnint=0
    for pair in table:
        continueyes=True
        while continueyes:
            if len(string)>=len(pair[0]):
                if string[0:len(pair[0])]==pair[0]:
                    returnint+=pair[1]
                    string=string[len(pair[0]):]
                else: 
                    continueyes=False
            else: 
                continueyes=False
    return returnint