from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('syg', 'sya')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    target = spicemanip(bot, triggerargsarray, 1)
    if not target:
        osd(bot, trigger.sender, 'say', "Screw you all, " + instigator + " is going home.")
    else:
        if target == bot.nick:
            osd(bot, trigger.sender, 'say', "Yeah, screw you too " + instigator + ".")
        elif target.lower() not in [u.lower() for u in bot.users]:
            osd(bot, trigger.sender, 'say', "Screw you guys, " + instigator + " is going home.")
        else:
            osd(bot, trigger.sender, 'say', "Screw you " + target + ", " + instigator + " is going home.")
