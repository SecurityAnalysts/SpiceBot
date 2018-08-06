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

# author jimender2


@sopel.module.commands('race')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'race')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    # setting up variables
    osd(bot, trigger.sender, 'say', "")
    instigator = trigger.nick
    command = get_trigger_arg(bot, triggerargsarray, 1)

    if command == "help":
        test
    elif command == "track":
        test
    elif command == "location":
        test
    elif command == "practice":
        test
    elif command == "random":
        test
    else:
        target = command
        # get the opposing person
        targetcheck = easytargetcheck(bot, botcom, target, instigator)
        if targetcheck == "instigator":
            osd(bot, trigger.sender, 'say', "Sorry dude. You cant race yourself.")
        elif targetcheck == "bot":
            osd(bot, trigger.sender, 'say', "I would let you race me but I am under Asimov's laws. Your feelings would be crushed by my winningness")
        elif targetcheck == "false":
            osd(bot, trigger.sender, 'say', "Dude, You cant race your imaginary friend ")
        elif targetcheck == "offline":
            osd(bot, trigger.sender, 'say', "You cannot race someone that is offline")
        elif targetcheck == "online":
            test


def race(bot, botcom, target, instigator):
    allUsers = [u.lower() for u in bot.users]
    user = get_trigger_arg(bot, allUsers, "random") or ''
