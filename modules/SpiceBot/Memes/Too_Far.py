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


@sopel.module.commands('toofar')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'toofar')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    item = spicemanip(bot, triggerargsarray, 0)
    firstitem = spicemanip(bot, triggerargsarray, 1)
    substring = spicemanip(bot, triggerargsarray, '2+') or 'empty'
    if not item:
        message = "What can you risk going too far?"
    else:
        if firstitem.endswith('ing') and substring != 'empty':
            itema = item
            itemb = firstitem.replace('ing', '') + ' ' + substring
        elif firstitem.endswith('e') and substring != 'empty':
            itema = firstitem[:-1]+"ing" + ' ' + substring
            itemb = item
        elif not item.endswith('ing'):
            itema = str(item + "ing")
            itemb = item
        else:
            itema = item
            itemb = item.replace('ing', '')
        message = "Only those people who risk " + str(itema) + " too far, ever find out how far they can " + str(itemb) + "!"
    osd(bot, trigger.sender, 'say', message)
