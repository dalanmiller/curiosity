import pluginapi
import urllib2
from bs4 import BeautifulSoup

NAME = "TodaysJoke"

_message_tracker = None


def initialize(skype):
    global _message_tracker
    _message_tracker = pluginapi.MessageTracker(skype, "RecentChats", "RecentMessages")


def execute(skype):
    global _message_tracker, _table
    unread_messages = _message_tracker.get_unread_messages()
    for msg in unread_messages:
        body = msg.Body.encode('ascii', 'replace')
        if body == "!joke":
            title, content = None, None

            req = urllib2.Request("http://www.reddit.com/r/Jokes/top/?sort=top&t=day", headers={'User-agent': 'Today\'s Joke'})
            con = urllib2.urlopen(req)
            page = BeautifulSoup(con.read())
            title_tag = page.find("a", "title")
            title = title_tag.string

            submission_url = "http://www.reddit.com" + title_tag['href']
            req = urllib2.Request(submission_url, headers={'User-agent': 'Today\'s Joke'})
            con = urllib2.urlopen(req)
            page = BeautifulSoup(con.read())
            expando = page.find("div", "expando")
            content = u"\n".join([unicode(p.string) for p in expando.findAll("p")])

            msg.Chat.SendMessage(unicode(title.upper()) + u"\n" + content)


def kill(skype):
    pass

if __name__ == '__main__':
    pass
