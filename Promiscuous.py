import sopel.module
from random import random
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('sexbot','cockbot','fuckbot')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    rando = randint(2, 22)
    bot.say("Please insert " + str(rando) + " bitcoins, for that kind of service.")
