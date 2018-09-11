#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2


@sopel.module.commands('piglatin', 'pl')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'piglatin')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick

    pyg = 'ay'
    firstsarray = ['a', 'e', 'i', 'o', 'u']

    rebuildarray = []
    if len(triggerargsarray) > 0:
        for word in triggerargsarray:
            word = word.lower()
            first = word[:1]
            if first in firstsarray:
                new_word = word + pyg
            else:
                new_word = word[1:] + first + pyg
            rebuildarray.append(new_word)
        words = get_trigger_arg(bot, rebuildarray, 0)
        osd(bot, trigger.sender, 'say', words)
    else:
        osd(bot, trigger.sender, 'say', "Oink oink")
