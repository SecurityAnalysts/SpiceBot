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


@sopel.module.commands('nelson')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'nelson')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = spicemanip(bot, triggerargsarray, 1)
    isvalid, validmsg = targetcheck(bot, botcom, target, instigator)
    if not target:
        message = "Who are we laughing at?"
    elif isvalid == 2:
        message = "Is your self esteem really that low?"
    elif isvalid == 0:
        message = "I'm not sure who that is."
    elif isvalid == 3:
        message = "I like to laugh, but not at my own expense."
    else:
        message = bot.nick + " points at " + target + " and laughs."
    osd(bot, trigger.sender, 'say', message)
