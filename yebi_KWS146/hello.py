from twitter import *
from konlpy.tag import Kkma
from konlpy.utils import pprint

t = Twitter(
    auth=OAuth(
        "531296598-Nqm9lzKTMyrJE0nlv7bMh7HlEbfUWg0jvF4V8kxI",
        "RSjhRBoah7zIKtxkB0ftXwfNU6NkjRX3zHaW3H9PCdM9H",
        "PYXCIBd6MbLvDj4c5GKs2u5KP",
        "au4ZSb77zWOzS5wvFICpoqqlwzshZDI2idv0JjdPoJX0lGe9Md"))

i = 1
kkma = Kkma()

for x in t.statuses.home_timeline(count=2):
    print "[" + str(i) + "]" + x['user']['screen_name'] + ": " + x['text']
    print "==============================================="
    pprint(kkma.nouns(x['text']))
    i += 1

