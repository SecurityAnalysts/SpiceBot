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

# author jimender2


@sopel.module.commands('upchuck')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'upchuck')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = spicemanip(bot, triggerargsarray, 1)
    instigator = trigger.nick
    rand = random.randint(1, 2)

    if not target:
        message = instigator + " throws up in their office."
    elif target == "all" or target == "everyone" or target == "everyones":
        message = instigator + " upchucks over everyone else."
    elif target == bot.nick:
        message = instigator + ". You can't do this. Neiner neiner"
    elif target == instigator:
        message = instigator + " leaves his shoes looking like Cambells soup. Chunky."
    elif rand == 1:
        message = instigator + " blows chunks onto " + target + ". " + target + " you can go home and clean up."
    elif rand == 2:
        message = instigator + " feels a little woozy and hits " + target + " with " + instigator + "'s lunch."
    else:
        message = "I screwed up majorly. You should never see this"

    osd(bot, trigger.sender, 'say', message)
