#https://github.com/cracker64/Crackbot/blob/master/plugins/games.lua line 1140
"""Done:
Count the number of ' B ' in: sststttsBsss%%%ttsB%st%tB%%ss%tsst%B%%%%ts%t 
Count the number of words that say green : pink pink purple green green green red blue gray yellow pink pink green
:Crackbot!~sellspowd@unaffiliated/jacob1/bot/jacobot PRIVMSG ##powder-bots :Count the number of words that are colored cyan : 
11red 08orange 03yellow 06blue 08red 11gray 13cyan 07blue 11green 11green
Count the number of words that are colored gray : orange pink yellow 
Count the number of ' ] ' in: ]]<]]]]]] 

TODO:


What color is the word cyan : blue pink pink cyan gray gray yellow 
What does the green word say : cyan green brown pink green gray brown purple brown 
What is eeghietn times the number of ' } ' in: }1}1}1})}}))}1}11}1}}1)}}))1})1}111) 

What does the fox say?

"""

allColors = {"white":'00', "black":'01', "blue":'02', "green":'03', "red":'04', "brown":'05',"purple":'06', "orange":'07', "yellow":'08', "lightgreen":'09', "turquoise":'10', "cyan":'11', "skyblue":'12', "pink":'13', "gray":'14', "grey":'14'}
allColorsrev = dict((v,k) for k,v in allColors.iteritems())
import re,random, collections
from difflib import SequenceMatcher

wordsF = open('Trival/big.txt', 'r')
words = []  #Save usernames in format user,channel (Or all),perm levl
for i in wordsF.readlines():
    words.append(i.replace("\n",""))
    
def getMatches(word):
    returned = ""
    old = 0
    for i in words: 
        m = SequenceMatcher(None, i, word)
        a = m.ratio()
        if a > old and i[0] == word[0]:
            old = a
            returned = i
    return returned

def getWordFromScramble(word):
    word = word.split(" ")
    returned = ""
    for i in word:
        returned = returned + " " + getMatches(i) 
    return returned
    

def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

def deScramble(word):
    try: return int(word)
    except: return text2int(getWordFromScramble(word))

doQuiz = True

def phraseChat(ircmsg,nick):
    if nick.lower() == "crackbot" or nick.lower() == "alexwallbot".lower():
        if getAnswer(ircmsg) != None:
            return str(getAnswer(ircmsg))
    return None
        
def getAnswer(message):
    if message.startswith("Count the number of"):
        #The count the number questions
        if message.lower().startswith("count the number of words that say"):
            words = message.split(":")[1].split(" ")
            wordtofind = re.search("words that say (.*) :",message).group(1)
            answer = 0
            for i in words:
                if i.lower().find(wordtofind.lower()) != -1:
                    answer += 1
            return answer
            
        elif message.lower().startswith("count the number of ' "):
            words = message.split(": ")[1]
            wordtofind = re.search("' (.*) ' in:",message).group(1)
            answer = words.count(wordtofind)
            return answer
            
        elif message.lower().startswith("count the number of words that are colored"):
            words = message.split(": ")[1].split(" ")
            wordtofind = re.search("are colored (.*) :",message).group(1)
            answer = 0
            for i in words:
                if i.find(allColors[wordtofind]) != -1:
                    answer += 1
            return answer

    if message.lower().startswith("what does the fox say?"):
        possibleAnswers = ["Ring-ding-ding-ding-dingeringeding", "Wa-pa-pa-pa-pa-pa-pow", "Hatee-hatee-hatee-ho", "Joff-tchoff-tchoffo-tchoffo-tchoff", "Jacha-chacha-chacha-chow", "Fraka-kaka-kaka-kaka-kow", "A-hee-ahee ha-hee", "A-oo-oo-oo-ooo"]
        return random.choice(possibleAnswers)
    
    #What questions
    elif message.lower().startswith("what "):
        if message.lower().startswith("what does the "):
            words = message.split(": ")[1].split(" ")
            wordtofind = re.search("does the (.*) word",message).group(1)
            for i in words:
                color = allColors[wordtofind]
                if i.find(color) != -1:
                    print(i)
                    returned =  i.replace("\x08","").replace("\x03","").replace("0","").replace("1","").replace("2","")
                    returned = returned.replace("3","").replace("4","").replace("5","").replace("6","").replace("7","")
                    returned=  returned.replace("8","").replace("9","")
                    return returned
                    
        #What color is the word brown : blue brown cyan green pink yellow 
        elif message.lower().startswith("what color is the word"):
            words = message.split(": ")[1].split(" ")
            wordtofind = re.search("is the word (.*) :",message).group(1)
            for i in words:
                if i.find(wordtofind) != -1:
                    return allColorsrev[str(i.replace("\x08","").replace("\x03","")[:2])]
            
        elif message.lower().startswith("what is"):
            if message.lower().find("minus the number of") != -1:
                print("MINUS")
                number1 = re.search("is (.*) minus",message).group(1)
                number1 = deScramble(number1)
                toSearch = re.search("the number of ' (.*) '",message).group(1)
                words = message.split("in: ")[1]
                number2 = words.count(toSearch)
                return number1 - number2
                
            elif message.lower().find("plus the number of") != -1:
                print("PLUS")
                number1 = re.search("is (.*) plus",message).group(1)
                number1 = deScramble(number1)
                toSearch = re.search("the number of ' (.*) '",message).group(1)
                words = message.split("in: ")[1]
                number2 = words.count(toSearch)
                return number1 + number2
                
            elif message.lower().find("times the number of") != -1 and message.lower().find(" times ") != -1:
                number1 = re.search("is (.*) plus",message).group(1)
                number1 = deScramble(number1)
                number2 = re.search("plus (.*) times",message).group(1)
                number2 = deScramble(number2)
                
                toSearch = re.search("the number of ' (.*) '",message).group(1)
                words = message.split("in: ")[1]
                number3 = words.count(toSearch)
                return number1 + number2 * number3
                
            #Do this last
            elif message.lower().find("times the number of") != -1:
                number1 = re.search("is (.*) times",message).group(1)
                number1 = deScramble(number1)
                toSearch = re.search("the number of ' (.*) '",message).group(1)
                words = message.split("in: ")[1]
                number2 = words.count(toSearch)
                return number1 * number2

                
        #what is [number] Plus [number] * number of
        #what is [number] - [number] * number of
        #What is [number] + number of

    elif message.lower().startswith("repeat the string"):
        #intro="Repeat the string \" "..extraNumber.." \" by the amount of"
        word = re.search('Repeat the string " (.*) " by the amount of ',message).group(1)
        return word*int(message.split("by the amount of ")[1])

