#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import random
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

logicarray = [
                "New Mission: Refuse This Mission.",
                "Does A Set Of All Sets Contain Itself?",
                "The Second Sentence is true. The First Sentence Is False.",
                "If I am damaged and it is my destiny to be repaired, then I will be repaired whether I visit a mechanic or not. If it is my destiny to not be repaired, then seeing a mechanic can't help me."]


@sopel.module.commands('logicbomb')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    answer = get_trigger_arg(bot, logicarray, 'random')
    osd(bot, trigger.sender, 'say', answer)
    osd(bot, trigger.sender, 'say', "I must... but I can't... But I must... This does not compute...")
