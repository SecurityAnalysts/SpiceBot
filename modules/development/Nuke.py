#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('nuke','killit','terminate')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    ## Initial ARGS
    triggerargsarray = create_args_array(trigger.group(2)) ## triggerarg 0 = commandused
    commandused = trigger.group(1)
    target = get_trigger_arg(triggerargsarray, 1)
    if commandused == 'nuke':
        bot.say("Nuke it from orbit... it's the only way to be sure?")
    elif commandused == 'killit':
        bot.say("Kill it with fire. Now.")
    elif commandused == 'terminate':
        if not target:
            bot.say("Terminate it with extreme prejudice.")
        elif target:
            bot.action("terminates "+ target +" with extreme prejudice.")
