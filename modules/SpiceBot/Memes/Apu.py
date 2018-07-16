#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import os
import sopel.module
import sys
import time
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('apu')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'apu')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)


def execute_main(bot, trigger, triggerargsarray):
    decide = random.randint(1,10)
    if decide == 1:
        message = "Who needs the Kwik-E-Mart? I do..."
        onscreentext(bot,['say'],message)
        time.sleep(2)
        actions = "starts crying"
        onscreentext_action(bot,['say'],actions)
    else:
        message = "Thank you, come again."
        onscreentext(bot,['say'],message)
