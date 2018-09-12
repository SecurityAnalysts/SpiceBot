#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import urllib
from xml.dom.minidom import parseString
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2


@sopel.module.commands('dankbonk')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'dankbonk')
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
    instigator = trigger.nick
    reason = spicemanip(bot, triggerargsarray, '2+')

    # no target
    if not target:
        message = "Who would you like to wack?"
    # target is spicebot
    elif target == bot.nick:
        message = "Spicebot teaches %s a lesson by sitting on %s" % (instigator, instigator)
    # target is the instigator
    elif target == instigator:
        message = "Sorry, I cannot let you harm yourself %s" % instigator
    # target is fine
    else:
        # no reason
        if not reason:
            message = "%s whacks %s with a 42 pound sack of primo cheeba." % (instigator, target)
        # reason
        else:
            message = "%s whacks %s with a 42 pound sack of primo cheeba because %s." % (instigator, target, reason)

    osd(bot, trigger.sender, 'say', message)
