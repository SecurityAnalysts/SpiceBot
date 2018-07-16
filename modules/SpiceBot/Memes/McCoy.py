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


@sopel.module.commands('mccoy')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'mccoy')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    doctorlines = ["I'm a doctor, Jim, I'm busy!","I don't need a doctor, damn it, I am a doctor!"]
    string = get_trigger_arg(bot, triggerargsarray, '1+')
    if string:
        if string == 'doctor':
            reply = get_trigger_arg(bot,doctorlines,'random')
            message = str(reply)
        else:
            message = "Dammit Jim, I'm a doctor, not a " + str(string) + "!!!"
    else:
        message = "He's dead, Jim."
    onscreentext(bot,['say'],message)
