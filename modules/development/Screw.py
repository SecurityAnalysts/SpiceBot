from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('syg','sya')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    target = get_trigger_arg(triggerargsarray, 1) or ''
    if target == '':
        bot.say("Screw you all, " + instigator + " is going home.")
    else:
        if target.lower() not in [u.lower() for u in bot.users]:
            bot.say("Screw someone, " + instigator + " is going home.")
        else:
            bot.say("Screw you " + target + ", " + instigator + " is going home.")
  
