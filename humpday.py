import sopel.module
import sys
import datetime

@sopel.module.commands('isitfriday','isitfridayyet')
def isitfriday(bot,trigger):
    whatistoday = str(datetime.datetime.today().weekday())        
    wednesdaynumber = '2'
    if whatistoday == wednesdaynumber:
        bot.say("Today is Wednesday, AKA HUMPDAY!!!!")
    else:
        bot.say("Today is not humpday.")
