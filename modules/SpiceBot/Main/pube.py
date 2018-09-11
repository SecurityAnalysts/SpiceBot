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


@sopel.module.commands('pube')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'pube')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    target = spicemanip(bot, triggerargsarray, 1)
    targetcheck = easytargetcheck(bot, botcom, target, instigator)

    if targetcheck == "instigator":
        osd(bot, trigger.sender, 'say', "Really?? You dont know if the curtains match the drapes!!")
    elif targetcheck == "bot":
        osd(bot, trigger.sender, 'say', "You know I dont care what you say")
    elif targetcheck == "false":
        allUsers = [u.lower() for u in bot.users]
        target = spicemanip(bot, allUsers, 0) or 'spicebot'
        osd(bot, trigger.sender, 'say', instigator + " wants to know if " + target + "'s carpets matches the drapes")
    elif targetcheck == "offline":
        osd(bot, trigger.sender, 'say', "You cannot ask someone that is offline")
    elif targetcheck == "online":
        osd(bot, trigger.sender, 'say', instigator + " wants to know if " + target + "'s carpets matches the drapes")
    else:
        allUsers = [u.lower() for u in bot.users]
        target = spicemanip(bot, allUsers, 0) or 'spicebot'
        osd(bot, trigger.sender, 'say', instigator + " wants to know if " + target + "'s carpets matches the drapes")
