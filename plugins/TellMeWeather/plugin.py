import urllib,urllib2, cookielib,urlparse
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup,UnicodeDammit
import Skype4Py
import pluginapi


NAME = "TellMeWeather"

currentTemp = ""
feelLikeTemp = ""
currentWind = ""
updateDate = ""
_message_tracker = None

def initialize(skype):
    global _message_tracker
    _message_tracker = pluginapi.MessageTracker(skype, "RecentChats", "RecentMessages")

def getWeather():
    response = getHtml("http://www.delfi.lt/orai/vilniaus-miestas/vilnius/")
    soup = BeautifulSoup(response)

    for div in soup.find_all('div', attrs={'class': 'dweather-current-location'}):
        for td in div.find_all('td'):
            if(td.has_key('class')):
                if("dweather-temp" in td["class"]):
                    currentTemp = td.string.encode("utf-8")
                if("dweather-feel-temp" in td["class"]):
                    for feel in td.div.find_all('div', attrs ={'class' : 'dweather-feel-value'}):
                        feelLikeTemp =  feel.string.encode("utf-8")
                if ("dweather-info-2" in td["class"]):
                    currentWind = td.div.get_text().encode("utf-8")

    message = "Dabartine temperatura: "+ currentTemp[0]+ "\n"+ "Jauciasi kaip: "+feelLikeTemp[0]+ "\nVejas: "+currentWind[len(currentWind)-9: len(currentWind)]
    return message

def execute(skype):
    global _message_tracker, _table
    unread_messages = _message_tracker.get_unread_messages()

    for msg in unread_messages:
        body = msg.Body.encode('ascii', 'replace')
        if(body =="!weather"):
            message = getWeather()
            msg.Chat.SendMessage(message)

def getHtml(url):
    f = urllib.urlopen(url)
    s = f.read()
    f.close()
    return s

def kill(skype):
    pass

if __name__ == '__main__':
    pass
