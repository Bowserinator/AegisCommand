import urllib
import requests, random
import xml.etree.ElementTree as ET


def wolfram(phrase):
    if phrase == "": return False
    phrase = urllib.quote(phrase)
    try:
        key = random.choice(["APLTT9-9WG78GYE65","VWJ4LK-PGJTQQEK63"])
        xml_data=requests.get("http://api.wolframalpha.com/v2/query?input="+phrase+"&appid="+key).text
        root = ET.fromstring(xml_data.encode('utf-8')) #.encode('ascii','ignore')
    
        amount = 0; returned = []
        for child in root:
            if amount < 1:
                amount += 1; current = {}
                current["title"] = child.get("title").encode('utf8')
                current["raw"] = []; current["img"] = [];
                for pod in root.findall('.//pod'):
                    for pt in pod.findall('.//img'):
                        current["img"].append( pt.get("src").encode('utf8') )
                    for pt in pod.findall('.//plaintext'):
                        if pt.text and pt.text.replace(" ","") != "":
                            current["raw"].append(pt.text.encode('utf8'))
                returned.append(current)
    
        return returned
    except:
        return False
