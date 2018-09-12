#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('sucker', 'suckers')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'sucker')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    myline = spicemanip(bot, triggerargsarray, 0)
    triggerword = spicemanip(bot, triggerargsarray, 1)
    if not myline:
        osd(bot, trigger.sender, 'say', "Who/what are for suckers??")
    elif bot.nick in myline:
        osd(bot, trigger.sender, 'say', "Do you really feel that way?")
    else:
        if myline.endswith('ing'):
            myline = str(myline + " is")
        if triggerword.endswith('ing'):
            myline = str(myline + " is")
        elif not myline.endswith('s'):
            myline = str(myline + "s are")
        else:
            myline = str(myline + " are")
        osd(bot, trigger.sender, 'say', myline + ' for suckers!!')
