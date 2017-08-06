import math

def rreplace(s, old, new, count):
    return (s[::-1].replace(old[::-1], new[::-1], count))[::-1]

def getRecipie(search, recipies):
    for key, value in recipies.iteritems(): #Key is item, Value is crafting recipie and stuff
        if search.lower() == key.lower():
            return value

def searchRecipie(search, recipies):
    if len(search) < 3:
        return "\x034" +"Search too short."
        
    results = []
    for key, value in recipies.iteritems(): #Key is item, Value is crafting recipie and stuff
        if search.lower() in key.lower():
            results.append(key)
            
    output = ""
    for i in results:
        output = output  + i + " ,"
    return rreplace(output,",","",1)
    
def getRecipieStr(search,recipies):
    returned = []
    recipie = getRecipie(search,recipies)
    empty_char = "_"
    
    word_length_max = 0
    for length in recipie[0]["recipe"]:
        if length != None:
            length = length.replace("Oak Wood Planks","Wood Planks")
        if length != None and len(length.replace(" ","-")) > word_length_max:
            word_length_max = len(length.replace(" ","-"))
    word_length_max += 2
    
    if word_length_max % 2 == 1:
        word_length_max += 1
    
    
    row1 = ""
    if recipie[0]["recipe"][0] == None and recipie[0]["recipe"][2] == None and recipie[0]["recipe"][1] == None:
        returned.append("")
    else:
        for i in range(0,2):
            item = recipie[0]["recipe"][i]
            if item == None:
                row1 = row1+empty_char  *word_length_max + "|"
            else:
                item = item.replace("Oak Wood Planks","Wood Planks")
                addNum = word_length_max - len(item.replace(" ","-"))
                addNum2 = len(item.replace(" ","-"))
                addNum = int(addNum/2)
                if addNum2 % 2 == 0:
                    row1 = row1 + addNum*empty_char   + item + addNum*empty_char   + "|"
                if addNum2 % 2 == 1:
                    row1 = row1 + addNum*empty_char   + item + addNum*empty_char + empty_char   + "|"
        item = recipie[0]["recipe"][2]
        if item == None:
            if recipie[0]["recipe"][2] == None and recipie[0]["recipe"][5] == None and recipie[0]["recipe"][8] == None:
                row1 = rreplace(row1,"|","",1)
            else:
                row1 = row1+empty_char  *(word_length_max)
        else:
            item = item.replace("Oak Wood Planks","Wood Planks")
            addNum = word_length_max - len(item.replace(" ","-"))
            addNum2 = len(item.replace(" ","-"))
            addNum = int(addNum/2)
            if addNum2 % 2 == 0:
                row1 = row1 + addNum*empty_char   + item + addNum*empty_char   
            if addNum2 % 2 == 1:
                row1 = row1 + addNum*empty_char   + item + addNum*empty_char + empty_char  
        returned.append(row1)
    
    ##ROW 2
    row2 = ""
    for i in range(3,5):
        item = recipie[0]["recipe"][i]
        if item == None:
            row2 = row2+empty_char  *(word_length_max) + "|"
        else:
            item = item.replace("Oak Wood Planks","Wood Planks")
            addNum = word_length_max - len(item.replace(" ","-"))
            addNum = int(addNum/2)
            addNum2 = len(item.replace(" ","-"))
            if addNum2 % 2 == 0:
                row2 = row2 + addNum*empty_char   + item + addNum*empty_char    + "|"
            if addNum2 % 2 == 1:
                row2 = row2 + addNum*empty_char   + item + addNum*empty_char + empty_char    + "|"
    item = recipie[0]["recipe"][5]
    if item == None:
        if recipie[0]["recipe"][2] == None and recipie[0]["recipe"][5] == None and recipie[0]["recipe"][8] == None:
            row2 = rreplace(row2,"|","",1)
        else:
            row2 = row2+empty_char  *(word_length_max)
    else:
        item = item.replace("Oak Wood Planks","Wood Planks")
        addNum = word_length_max - len(item.replace(" ","-"))
        addNum = int(addNum/2)
        addNum2 = len(item.replace(" ","-"))
        if addNum2 % 2 == 0:
            row2 = row2 + addNum*empty_char   + item + addNum*empty_char   
        if addNum2 % 2 == 1:
            row2 = row2 + addNum*empty_char   + item + addNum*empty_char + empty_char   
    returned.append(row2)
    
    ##ROW 3
    row3 = ""
    for i in range(6,8):
        item = recipie[0]["recipe"][i]
        if item == None:
            row3 = row3+empty_char  *(word_length_max) + "|"
        else:
            item = item.replace("Oak Wood Planks","Wood Planks")
            addNum = word_length_max - len(item.replace(" ","-"))
            addNum = int(addNum/2)
            addNum2 = len(item.replace(" ","-"))
            if addNum2 % 2 == 0:
                row3= row3 + addNum*empty_char   + item + addNum*empty_char    + "|"
            if addNum2 % 2 == 1:
                row3 = row3 + addNum*empty_char   + item + addNum*empty_char + empty_char    + "|"
    item = recipie[0]["recipe"][8]
    if item == None:
        if recipie[0]["recipe"][2] == None and recipie[0]["recipe"][5] == None and recipie[0]["recipe"][8] == None:
            row3 = rreplace(row3,"|","",1) + " (" + str(recipie[0]["output"]) + ")"
        else:
            row3 = row3+empty_char  *(word_length_max) + " (" + str(recipie[0]["output"]) + ")"
    else:
        item = item.replace("Oak Wood Planks","Wood Planks")
        addNum = word_length_max - len(item.replace(" ","-"))
        addNum = int(addNum/2)
        addNum2 = len(item.replace(" ","-"))
        if addNum2 % 2 == 0:
            row3 = row3 + addNum*empty_char   + item + addNum*empty_char   + " (" + str(recipie[0]["output"]) + ")"
        if addNum2 % 2 == 1:
            row3 = row3 + addNum*empty_char   + item + addNum*empty_char + empty_char   + " (" + str(recipie[0]["output"]) + ")"
    returned.append(row3)
    
    if returned[0] == "":
        if returned[1].split("|")[0].replace(" ","") == "" and returned[2].split("|")[0].replace(" ","") == "":
            returned[1] = "| " + returned[1].split("|",1)[1] + " |"
            returned[2] = "| " + returned[2].split("|",1)[1]
            
    return returned

def roundUp(numToRound, multiple):
    if (multiple == 0):
        return numToRound

    remainder = numToRound % multiple
    if (remainder == 0):
        return numToRound

    return numToRound + multiple - remainder


def RecipieCalc(search,recipies, amount):
    returned = []
    recipie = getRecipie(search,recipies)
    returned = ""
    if recipie != None:
        items = []
        for item in recipie[0]["recipe"]:
            items.append(item)
        item_unique = list(set(items))
        
        for item in item_unique:
            if item != None:
                amount = roundUp(amount,int(recipie[0]["output"]))
                returned = returned + str(math.ceil(int(items.count(item)*amount / math.ceil(recipie[0]["output"])))) + " " + item + "  "
        return returned
    return "Item not found, use @search."


            