import sopel
from sopel import module, tools
import random
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('blame')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    whotoblame = get_trigger_arg(triggerargsarray, 1)
    if not whotoblame:
        blametargetarray = []
        for channel in bot.channels:
            for u in bot.channels[channel].users:
                disenable = get_botdatabase_value(bot, u, 'disenable')
                if u != instigator and u != bot.nick:
                    blametargetarray.append(u)
        if blametargetarray == []:
            whotoblame = str(instigator + "'s mom")
        else:
            whotoblame = get_trigger_arg(blametargetarray, 'random')
            bot.say("It's " + whotoblame + "'s fault.")
    elif whotoblame.lower() not in bot.privileges[channel.lower()]:
        bot.say("I'm not sure who that is.")
    else:
        bot.say("It's " + whotoblame + "'s fault.")
