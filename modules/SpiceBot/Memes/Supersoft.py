#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('supersoft')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'supersoft')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = get_trigger_arg(bot, triggerargsarray, 1)
    isvalid, validmsg = targetcheck(bot, botcom, target, instigator)
    channel = trigger.sender
    if not target:
        message = "Who is supersoft?"
    elif target == instigator:
        message = "Is your self esteem really that low?"
    elif isvalid == 0:
        message = "I'm not sure who that is."
    elif isvalid == 3:
        message = "I'm all metal, baby"
    else:
        pick = random.randint(1, 10)
        if pick == 1:
            message = target + " is going to have a super soft birthday party this year."
        else:
            message = target + " is supersoft. 10-ply. Now give your balls a tug, tit-fucker and figger it out. Ferda!"
    osd(bot, trigger.sender, 'say', message)
