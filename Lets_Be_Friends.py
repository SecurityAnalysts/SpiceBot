import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.rate(120)
@sopel.module.commands('fuckyouspicebot','fuckspicebot','banspicebot','kickspicebot','hatespicebot','fuckoffspicebot')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    bot.say(trigger.nick + ", I'm sorry I offended you. Lets try to be friends.")
