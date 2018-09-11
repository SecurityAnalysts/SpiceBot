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


@sopel.module.commands('homer')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'homer')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    goodarray = ['good', 'g']
    badarray = ['bad', 'b', 'bad?', 'good?']
    goodorbad = spicemanip(bot, triggerargsarray, 0) or 'bad'
    if goodorbad in goodarray:
        message = "WooHoo!"
    elif goodorbad in badarray:
        message = "D'ooooh!"
    else:
        message = str("mmmmmmm " + goodorbad + "!")
    osd(bot, trigger.sender, 'say', message)
