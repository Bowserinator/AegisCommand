import requests, urllib, re

def define(x):
    """define word <definition number=1 and 2>"""
    x = x.lower().replace("/","").replace("&","").replace("\\","").replace("#","")

    if x == "pulling an indigotiger": return ["Speaking only when needed, coined by BWBellairs."]
    elif x in ["bowser","bowserinator"]: return ["Bowserinator, the creator of this bot."]
    elif x == "hippopotomonstrosesquipedaliophobia": return ["A fear of long words, too bad dictionary.com can't define this."]
    elif x == "bwbellairs": return ["A person who says your instead of you're."]
    elif x == "jeffl35": return ["Someone insignificant who ruins your code."]
    elif x == "moony": return ["Someone you ask to fix their shit.","A cow with a brain."]
    elif x == "pocketbot": return ["POOP (Php Object Oriented Programming)"]
    elif x == "handicraftsman": return ["fuk u"]
    definitions = []
    
    x = urllib.quote(x)
    result = requests.get("http://www.dictionary.com/browse/"+x+"?s=t").text
    print re.findall('<divclass="def-set"><spanclass="def-number">(.*?)</span>',result.replace("\n","").replace(" ",""))
    for i in re.findall('<div class="def-content">(.*?)</div>',result.replace("\n","")):
        if i.lstrip().rstrip()[0] not in list("(</"):
            result = i.split("<div")[0].split("<span")[0]
            result = result.replace('<div class="def-block def-inline-example"><span class="dbox-example">','')
            result = result.replace("</span>","").replace("<span>","")
            if result.replace(" ","") != "": definitions.append(result.lstrip().rstrip())
    
    new_def = []   
    for x in definitions:
        x = x.replace("\x01","")
        x = re.sub('>(.*?)</a>',"\1",x)
        x = re.sub('<a class="dbox-xref dbox-roman" href="http://www.dictionary.com/browse/(.*?)','"\1',x)
        new_def.append(x)
    return new_def

import urllib2

def translate(to_translate, to_langage="auto", langage="auto"):
    #Translate <text> to_lan=<test> from_lan=<test>
	to_translate = to_translate.replace("/","").replace("%","").replace("$","")
	agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
	before_trans = 'class="t0">'
	link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_langage, langage, to_translate.replace(" ", "+"))
	request = urllib2.Request(link, headers=agents)
	page = urllib2.urlopen(request).read()
	result = page[page.find(before_trans)+len(before_trans):]
	result = result.split("<")[0]
	
	result = result.replace("&quot;",'"').replace("&#39;","'").replace("&lt","<").replace("&gt;",">")
	return "\x02Result: \x0f" +  result