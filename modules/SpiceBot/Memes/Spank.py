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

spankweapons = ['paddle', 'belt']


@sopel.module.commands("spank", "paddle", "paddlin")
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'spank')
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
    reason = spicemanip(bot, triggerargsarray, '2+')
    message = "Whoops, something went wrong."
    # Nothing specified
    if not target:
        message = "Thaat's a paddlin'"

    # Can't slap the bot
    elif target == bot.nick:
        message = "I will not do that!!"

    # Target is fine
    else:
        weapon = spicemanip(bot, spankweapons, 'random')
        if not reason:
            message = trigger.nick + " spanks " + target + " with a " + weapon + "."
        else:
            if reason.startswith('for'):
                message = trigger.nick + " spanks " + target + " with a " + weapon + " " + reason + "."
            else:
                message = trigger.nick + " spanks " + target + " with a " + weapon + " " + reason + "."
    osd(bot, trigger.sender, 'say', message)
