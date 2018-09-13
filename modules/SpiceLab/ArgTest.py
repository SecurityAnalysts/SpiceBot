import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.require_admin
@sopel.module.commands('argtest')
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
    arraytest = ['main']
    if isinstance(arraytest, list):
        osd(bot, trigger.sender, 'say', 'array is an array')
    else:
        osd(bot, trigger.sender, 'say', 'array is not an array')
    notarraytest = "not an array"
    if isinstance(notarraytest, list):
        osd(bot, trigger.sender, 'say', 'notarray is an array')
    else:
        osd(bot, trigger.sender, 'say', 'notarray is not an array')
    channelarray = []
    for c in bot.channels:
        channelarray.append(c)
    channel = spicemanip(channelarray, 0)
    osd(bot, trigger.sender, 'say', str(channel))
    totalarray = len(triggerargsarray)
    totalarray = totalarray + 1
    simulatedvaluearray = ['5+', '5-', '5<', '5>', 'last', '5^7', '5!', 'random', 'list']
    for i in range(0, totalarray):
        arg = spicemanip(triggerargsarray, i)
        osd(bot, trigger.sender, 'say', "arg " + str(i) + " = " + str(arg))
    for x in simulatedvaluearray:
        value = spicemanip(triggerargsarray, x)
        if value != '':
            osd(bot, trigger.sender, 'say', "arg " + str(x) + " = " + str(value))
        else:
            osd(bot, trigger.sender, 'say', "arg " + str(x) + " is empty")
