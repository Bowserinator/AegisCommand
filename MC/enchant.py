"""
From http://minecraft.gamepedia.com/Enchantment_mechanics


Then find possible enchantments for item based on level:
http://minecraft.gamepedia.com/Enchanting\Levels

Get enchantment based on "weight"

Check for conflits
"""

import math,random

def generateBaseLevel(slot,books): #1 = top, 2 = middle, etc...
    base = random.randint(1,8) + math.floor(books/2) + random.randint(0,books)
    if slot == 1:
        return max(base/3,1)
    elif slot == 2:
        return (base * 2) / 3 + 1
    elif slot == 3:
        return max(base,books*2)

def getLevel(tool,base):
    returned = 0
    
    if tool in ["wooden axe","wooden pickaxe","wooden hoe","wooden shovel","wooden sword"]:
        enchant = 15
        returned = base + random.uniform(0, enchant/4) + random.uniform(0, enchant/4) + 1
    elif tool in ["leather helmet","leather chestplate","leather leggings","leather boots"]:
        enchant = 15
        returned = base + random.uniform(0, enchant/4) + random.uniform(0, enchant/4) + 1
    elif tool in ["stone axe","stone pickaxe","stone hoe","stone shovel","stone sword"]:
        enchant = 5
        returned = base + random.uniform(0, enchant/4) + random.uniform(0, enchant/4) + 1
    elif tool in ["iron helmet","iron chestplate","iron leggings","iron boots"]:
        enchant = 9
        returned = base + random.uniform(0, enchant/4) + random.uniform(0, enchant/4) + 1
    elif tool in ["iron axe","iron pickaxe","iron hoe","iron shovel","iron sword"]:
        enchant = 14
        returned = base + random.uniform(0, enchant/4) + random.uniform(0, enchant/4) + 1
    elif tool in ["chain helmet","chain chestplate","chain leggings","chain boots"]:
        enchant = 12
        returned = base + random.uniform(0, enchant/4) + random.uniform(0, enchant/4) + 1
    elif tool in ["diamond helmet","diamond chestplate","diamond leggings","diamond boots"]:
        enchant = 10
        returned = base + random.uniform(0, enchant/4) + random.uniform(0, enchant/4) + 1
    elif tool in ["diamond axe","diamond pickaxe","diamond hoe","diamond shovel","diamond sword"]:
        enchant = 10
        returned = base + random.uniform(0, enchant/4) + random.uniform(0, enchant/4) + 1
    elif tool in ["gold helmet","gold chestplate","gold leggings","gold boots"]:
        enchant = 25
        returned = base + random.uniform(0, enchant/4) + random.uniform(0, enchant/4) + 1
    elif tool in ["gold axe","gold pickaxe","gold hoe","gold shovel","gold sword"]:
        enchant = 22
        returned = base + random.uniform(0, enchant/4) + random.uniform(0, enchant/4) + 1
    elif tool in ["bow","book","fishing rod"]:
        enchant = 1
        returned = base + random.uniform(0, enchant/4) + random.uniform(0, enchant/4) + 1
    
    return round(random.uniform(0.85,1.15) * math.floor(returned))


class Enchantment:
    def __init__(self,name,level,enchant_range):
        self.name = name
        self.level = level
        self.enchant_range = enchant_range

enchantments_armor = [
    Enchantment("Protection",1,[1,21]),
    Enchantment("Protection",2,[12,32]),
    Enchantment("Protection",3,[18,30]),
    Enchantment("Protection",4,[34,54]),
    Enchantment("Fire Protection",1,[10,22]),
    Enchantment("Fire Protection",1,[18,30]),
    Enchantment("Fire Protection",1,[26,38]),
    Enchantment("Fire Protection",1,[34,46]),
    Enchantment("Feather Falling",1,[5,15]),
    Enchantment("Feather Falling",1,[11,21]),
    Enchantment("Feather Falling",1,[17,27]),
    Enchantment("Feather Falling",1,[23,33]),
    Enchantment('Blast Protection',1,[5,17]), 
    Enchantment('Blast Protection',2,[13,15]), 
    Enchantment('Blast Protection',3,[21,33]), 
    Enchantment('Blast Protection',4,[29,41]), 
    Enchantment('Projectile Protection',1,[3,18]), 
    Enchantment('Projectile Protection',2,[9,24]), 
    Enchantment('Projectile Protection',3,[15,30]), 
    Enchantment('Projectile Protection',4,[21,36]), 
    Enchantment('Resperation',1,[10,40]), 
    Enchantment('Resperation',2,[20,50]), 
    Enchantment('Resperation',3,[30,60]), 
    Enchantment('Aqua Affinity',1,[1,41]), 
    Enchantment('Thorns',1,[10,60]),
    Enchantment('Thorns',2,[30,80]), 
    Enchantment('Thorns',3,[50,100]), 
    Enchantment('Depth Strider',1,[10,25]),
    Enchantment('Depth Strider',2,[20,35]),
    Enchantment('Depth Strider',3,[30,45]),
]

enchantments_sword = [
    Enchantment('Sharpness',1,[1,21]),
    Enchantment('Sharpness',2,[12,32]),
    Enchantment('Sharpness',3,[23,43]),
    Enchantment('Sharpness',4,[34,54]),
    Enchantment('Sharpness',5,[45,65]),
    Enchantment('Smite',1,[5,25]),
    Enchantment('Smite',2,[13,33]),
    Enchantment('Smite',3,[21,41]),
    Enchantment('Smite',4,[29,49]),
    Enchantment('Smite',5,[37,57]),
    Enchantment('Bane of Arthropods',1,[5,25]),
    Enchantment('Bane of Arthropods',2,[13,33]),
    Enchantment('Bane of Arthropods',3,[21,41]),
    Enchantment('Bane of Arthropods',4,[29,49]),
    Enchantment('Bane of Arthropods',5,[37,57]),
    Enchantment('Knockback',1,[5,55]),
    Enchantment('Knockback',2,[25,75]),
    Enchantment('Fire Aspect',1,[10,60]),
    Enchantment('Fire Aspect',2,[30,80]),
    Enchantment('Looting',1,[15,65]),
    Enchantment('Looting',2,[24,74]),
    Enchantment('Looting',3,[33,83])
]

enchantments_bow = [
    Enchantment('Power',1,[1,16]),
    Enchantment('Power',2,[11,26]),
    Enchantment('Power',3,[21,36]),
    Enchantment('Power',4,[31,46]),
    Enchantment('Power',5,[41,56]),
    Enchantment('Punch',1,[12,37]),
    Enchantment('Punch',2,[32,57]),
    Enchantment('Flame',1,[20,50]),
    Enchantment('Infinity',1,[20,50]),
]

enchantments_tool = [
    Enchantment('Efficiency',1,[1,51]),
    Enchantment('Efficiency',2,[11,61]),
    Enchantment('Efficiency',3,[21,71]),
    Enchantment('Efficiency',4,[31,81]),
    Enchantment('Efficiency',5,[41,91]),
    Enchantment('Silk Touch',1,[15,65]),
    Enchantment('Unbreaking',1,[5,55]),
    Enchantment('Unbreaking',2,[13,63]),
    Enchantment('Unbreaking',3,[21,71]),
    Enchantment('Fortune',1,[15,65]),
    Enchantment('Fortune',2,[24,74]),
    Enchantment('Fortune',3,[33,83])
]

enchantments_rod = [
    Enchantment('Luck of the Sea',1,[1,65]),
    Enchantment('Luck of the Sea',2,[24,74]),
    Enchantment('Luck of the Sea',3,[33,83]),
    Enchantment('Lure',1,[1,65]),
    Enchantment('Lure',2,[24,74]),
    Enchantment('Lure',3,[33,83]),
]

def getPossibleEnchants(tool,slot,books):
    level = getLevel(tool,generateBaseLevel(slot,books))
    possible = []
    
    #If 2 same enchants, choose higher level
    if tool.lower().find("sword") != -1: #Sword
        for i in enchantments_sword:
            if i.enchant_range[0] <= level <= i.enchant_range[1]:
                possible.append(i)
    elif tool.lower().find("fishing rod") != -1: #Rod
        for i in enchantments_rod:
            if i.enchant_range[0] <= level <= i.enchant_range[1]:
                possible.append(i)
    elif tool.lower().find("bow") != -1: #Bow
        for i in enchantments_bow:
            if i.enchant_range[0] <= level <= i.enchant_range[1]:
                possible.append(i)
    elif tool.lower().find("chestplate") != -1 or tool.lower().find("leggings") != -1 or tool.lower().find("leggings") != -1 or tool.lower().find("helmet") != -1: #Armor
        for i in enchantments_armor:
            if i.enchant_range[0] <= level <= i.enchant_range[1]:
                possible.append(i)
    else:
        for i in enchantments_tool:
            if i.enchant_range[0] <= level <= i.enchant_range[1]:
                possible.append(i)
    
    #Remove weak enchantments
    to_remove = []
    for x in possible:
        for y in possible:
            if y.name == x.name and y.level < x.level:
                to_remove.append(y)
    for p in to_remove:
        if p in possible:
            possible.remove(p)
            
    return possible
    
def getEnchants(tool,slot,books):
    enchants = getPossibleEnchants(tool,slot,books)
    returned = []
    keepGoing = True
    
    while keepGoing:
        if tool.lower().find("chestplate") != -1 or tool.lower().find("leggings") != -1 or tool.lower().find("leggings") != -1 or tool.lower().find("helmet") != -1: #Armor
            choice = random.choice([
                "Protection","Protection","Protection","Protection","Protection","Protection","Protection","Protection","Protection","Protection",
                "Feather Falling","Feather Falling","Feather Falling","Feather Falling","Feather Falling",
                "Fire Protection","Fire Protection","Fire Protection","Fire Protection","Fire Protection",
                "Projectile Protection","Projectile Protection","Projectile Protection","Projectile Protection","Projectile Protection",
                "Aqua Affinity","Aqua Affinity",
                "Blast Protection","Blast Protection",
                "Respiration","Respiration",
                "Depth Strider","Depth Strider",
                "Thorns"
            ])
        elif tool.lower().find("sword") != -1: #Sword
            choice = random.choice([
                "Sharpness","Sharpness","Sharpness","Sharpness","Sharpness","Sharpness","Sharpness","Sharpness","Sharpness","Sharpness",
                "Bane of Arthropods","Bane of Arthropods","Bane of Arthropods","Bane of Arthropods","Bane of Arthropods",
                "Knockback","Knockback","Knockback","Knockback","Knockback",
                "Smite","Smite","Smite","Smite","Smite",
                "Fire Aspect","Fire Aspect",
                "Looting","Looting"
            ])
        elif tool.lower().find("bow") != -1: #Bow
            choice = random.choice([
                "Power","Power","Power","Power","Power","Power","Power","Power","Power","Power",
                "Flame","Flame",
                "Punch","Punch",
                "Infinity"
            ])
        elif tool.lower().find("fishing rod") != -1: #Rod
            choice = random.choice([
                "Luck of the Sea","Luck of the Sea","Lure","Lure"
            ])
        else:
            choice = random.choice([
                "Efficiency","Efficiency","Efficiency","Efficiency","Efficiency","Efficiency","Efficiency","Efficiency","Efficiency","Efficiency",
                "Unbreaking","Unbreaking","Unbreaking","Unbreaking","Unbreaking",
                "Fortune","Fortune",
                "Silk Touch"
            ])
        
        for x in enchants:
            if x.name.lower() == choice.lower():
                returned.append(x)
        if len(returned) != 0:
            if random.random > (getLevel(tool,generateBaseLevel(slot,books))+1)/50:
                keepGoing = False
    
    returned = list(set(returned))
    return returned

#calculate prob to get [enchant] on [item]
def getProbEnchant(enchant,tool,slot,bookshelves):
    total = 0
    match = 0
    for i in range(0,500): #100 tests arne't bad
        a = getEnchants(tool,slot,bookshelves)
        for x in a:
            x_name = x.name.lower() + " " + str(x.level)
            if x_name.find(enchant.lower()) != -1:
                match += 1
            total += 1
    return match/float(total)
    
def getBestSlot(enchant,tool,books):
    #Loop through 3 slots, for the best option of getting it.
    old_choice = [0,0] #Slot number, result
    for i in [1,2,3]:
        a = getProbEnchant(enchant,tool,i,books)
        if a > old_choice[1]:
            old_choice = [i,a]
    return old_choice
    
def getBestLevel(enchant,tool):
    #Loop through book shelves, then slot number
    old_choice = [0,0,0] #Book, slot, prob
    for i in range(0,10):
        for i in range(16):
            for x in [1,2,3]:
                a = getProbEnchant(enchant,tool,x,i)
                if a > old_choice[1]:
                    old_choice = [i,x,a]
    return old_choice


def getToolStats(tool,enchants):
    enchants = enchants.split(",")
    returned = []
    
    durability = 0
    damage = 0 #In half hearts, so 20 damage = 10 hearts of damage
    
    if tool.lower().find("diamond") != -1:
        durability = 1562
        damage = 8
    elif tool.lower().find("iron") != -1:
        durability = 251
        damage = 7
    elif tool.lower().find("stone") != -1:
        durability = 132
        damage = 6
    elif tool.lower().find("wood") != -1:
        durability = 60
        damage = 5
    elif tool.lower().find("gold") != -1:
        durability = 33
        damage = 5
            
    if tool.lower().find("sword") != -1:
        for enchant in enchants:
            enchant2 = enchant.rsplit(" ",1)
            if enchant2[0].lower().find("sharpness") != -1:
                returned.append("New: " + str(float(enchant2[1]) * 1.25/2 + damage) + " heart damage.")
            elif enchant2[0].lower().find("knockback") != -1:
                returned.append("New: " + str(float(enchant2[1]) * 3) + " block knockback.")
            elif enchant2[0].lower().find("fire aspect") != -1:
                returned.append("New: " + str(float(enchant2[1]) * 4 - 1) + " fire damage.")
            elif enchant2[0].lower().find("unbreaking") != -1:
                returned.append("New: " + str((float(enchant2[1])+1)*durability) + " uses.")
    elif tool.lower().find("pickaxe") != -1:
        for enchant in enchants:
            enchant2 = enchant.rsplit(" ",1)
            if enchant2[0].lower().find("fortune") != -1:
                returned.append("Varies per block, see http://goo.gl/RA5oih for more info")
            elif enchant2[0].lower().find("unbreaking") != -1:
                returned.append("New: " + str((float(enchant2[1])+1)*durability) + " uses.")    
                
    elif tool.lower().find("fishing rod") != -1:
        if enchant2[0].lower().find("luck of the sea") != -1:
            returned.append("+: " + str(float(enchant2[1]) * 1.01) + " * chance of treasure.")
            returned.append("-: " + str(float(enchant2[1]) * 1.025) + " * chance of junk.")
        elif enchant2[0].lower().find("lure") != -1:
            returned.append("-: " + str(float(enchant2[1]) * 5) + " * seconds wait time.")
            returned.append("-: " + str(float(enchant2[1]) * 1.01) + " * chance of junk and treasure.")
            
    elif tool.lower().find("bow") != -1:
        if enchant2[0].lower().find("flame") != -1:
            returned.append("New: 2.5 hearts fire damage.")
        elif enchant2[0].lower().find("power") != -1:
            returned.append("New: " + str(1.25*(float(enchant2[1]) +1)/2 + 2) + " hearts damage.")
            
            
    if tool.lower().find("shovel") != -1 or tool.lower().find("axe") != -1 or tool.lower().find("pickaxe") != -1:
        if enchant2[0].lower().find("efficency") != -1:
            returned.append("New: " + str(float(enchant2[1]) * 1.3) + " * mining speed (Must use correct tool).")
            
    return returned

#a = getToolStats("diamond sword","unbreaking 1,sharpness 5,knockback 1,fire aspect 2")
#print(a)