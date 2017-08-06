import requests, json, urllib, re, urllib2

class UrlShortenError(Exception):
    pass
class NoTitleError(Exception):
    pass
class YoutubeError(Exception):
    pass

class Web(object):
    def __init__(self):
        pass
    
    def paste(self,string):
        """Makes a hastebin for the string, returns the url"""
        returned = requests.post("http://hastebin.com/documents", data=string)
        return "http://hastebin.com/"+returned.json()['key']
    
    def tinyurl(self,url):
        """Makes shortened url with tinyurl"""
        try:
            tiny_url = "http://tinyurl.com/api-create.php?url={0}".format(url)
            page = requests.get(tiny_url).text
            return page
        except: raise UrlShortenError("Unable to shorten the following url - {0}".format(url))
        
    def isgd(self,url,keyword=None):
        """Makes shortened url with isgd, optional keyword to make meaningful url instead of random characters"""
        try:    
            isgdurl = 'http://is.gd/create.php?format=simple&url=' + urllib.quote(url)
            if keyword: isgdurl += '&shorturl=' + keyword
            page = requests.get(isgdurl).text
    
            #Check if it works
            isgdurl = 'http://is.gd/forward.php?format=simple&shorturl=' + page
            requests.get(isgdurl)
        except: raise UrlShortenError("Unable to shorten the following url - {0}".format(url))
        return page
        
    def title(self,url):
        """Gets title of the url, useful for getting an idea of what the website is about"""
        text = requests.get(url).text
        result = re.findall("<title>(.*?)</title>",text)
        if len(result) > 0: return result[0]
        raise NoTitleError("Failed to obtain the title of the following url: {0}".format(url))
        
    def expandUrl(self,url):
        """Unshortens a shortened url"""
        session = requests.Session() 
        result = session.head(url, allow_redirects=True)
        return result.url
        
    def youtube(self,url):
        """Gets information for youtube video"""
        try:
            data = requests.get(url).text
            title = re.findall("<title>(.*?)</title>",data)[0]
            desc = re.findall('<meta name="description" content="(.*?)">',data)[0]
            image = re.findall('<meta property="og:image" content="(.*?)">',data)[0]
            views = re.findall('<div class="watch-view-count">(.*?)</div>',data)[0]
            views = int(views.replace("views","").replace(",",""))
            return {"name":title, "desc":desc, "image":image, "views":views}
        except: raise YoutubeError("Could not get video data for url - {0}".format(url))
        
    def latex(self,equation,file):
        """Renders an latex equation and saves it to file"""
        r = requests.get("http://latex.codecogs.com/png.latex?\dpi{300} \huge "+equation)
        f = open( file, 'wb+' )
        f.write(r.content ); f.close()
        
