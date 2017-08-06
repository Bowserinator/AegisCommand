#Gets pastebin title, user, post, file size, expire date
import requests,re
import urllib
import json, time

try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

h = HTMLParser()

def getTitleURL(message):
    message = message.lower()
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    #if "." in urls[0].split("/")[-1] and urls[0].count("/") > 2: #No files :)
        #return "\x02[Unknown title]"

    try: 
        t2 = requests.get( urls[0], timeout=4, stream=True)
    except Exception as e: 
        return ""
    
    max_size = 100000+1
    
    #if int(t2.headers.get('Content-Length')) > max_size:
        #return "\x02[Response too large]"

    size = 0
    start = time.time()
    t = t2.raw.read(100000+1, decode_content=True)
    
    for chunk in t2.iter_content(1024):
        if time.time() - start > 4000:
            return ""
    
        size += len(chunk)
        if size > max_size:
            return "\x02[Response too large]"

    if "title" not in t:
        return "[No title]"
    return "\x02[Title]\x0f " + h.unescape( re.findall("title[^>]*>([^<]*)</title\s*>", t ) [0].encode('utf-8').replace("\\x","").replace("\n","").replace("\r","")[:250] )
    
def getYoutube(url):
    #youtube = etree.HTML(urllib.urlopen(url).read()) #enter your youtube url here
    #video_title = youtube.xpath("//span[@id='eow-title']/@title") #get xpath using firepath firefox addon
    return h.unescape( re.findall("<title>(.*?)</title>", requests.get( url ).text ) [0] )
    
def getTPT(saveId):
    page = requests.get("http://powdertoy.co.uk/Browse/View.html?ID=" + str(saveId))
    try:
        if page != None:
            page = page.text
    
            title = re.search('<meta property="og:title" content=(.*) />',page).group(1).replace('"',"")
            likesTotal = re.search('<span class="ScoreLike badge badge-success">(.*)</span>',page).group(1).split('</span>&nbsp;/&nbsp;<span class="ScoreDislike badge badge-important">')
            likes = likesTotal[0]
            dislikes = likesTotal[1]
            return "Save " + saveId + " is " + h.unescape(title) + " and has " + likes + " likes and " + dislikes + " dislikes."
    except:
        return ""


def getThread(threadId):
    threadId = threadId.replace(":","").replace(".","")
    jsonD = requests.get("http://powdertoy.co.uk/Discussions/Thread/View.json?Thread="+str(threadId)).text
    if jsonD == '{"Status":"0","Error":"The thread you have tried to view does not exist"}':
        return ""
    data = json.loads(jsonD)
    returned = "Thread is '"

    topic = data["Info"]["Topic"]
    returned = returned + topic["Title"] + "' by " + topic["Author"]
    returned = returned + " has " + str(topic["PostCount"]) + " posts and " + str(topic["ViewCount"]) + " views. Last post by " + topic["LastPoster"] + " on " + str(topic["Date"]) 
    return returned
