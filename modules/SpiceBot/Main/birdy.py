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


@sopel.module.commands('birdy')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    rand = random.randint(1,20)
    if rand == 1:
        osd(bot, trigger.sender, 'say', "_________$$____________")
        osd(bot, trigger.sender, 'say', "________$__$___________")
        osd(bot, trigger.sender, 'say', "________$__$___________")
        osd(bot, trigger.sender, 'say', "_______$$__$$__________")
        osd(bot, trigger.sender, 'say', "______$__$__$_$$_$$____")
        osd(bot, trigger.sender, 'say', "______$__$__$__$$__$___")
        osd(bot, trigger.sender, 'say', "_$$$__$__$__$__$$__$___")
        osd(bot, trigger.sender, 'say', "$___$$_______________$_")
        osd(bot, trigger.sender, 'say', "$____$$_______________$")
        osd(bot, trigger.sender, 'say', "_$____________________$")
        osd(bot, trigger.sender, 'say', "__$___________________$")
        osd(bot, trigger.sender, 'say', "___$_________________$_")
        osd(bot, trigger.sender, 'say', "____$_______________$__")
        osd(bot, trigger.sender, 'say', "_____$_____________$___")
        osd(bot, trigger.sender, 'say', "______$___________$____")
        osd(bot, trigger.sender, 'say', "_______$$$$$$$$$$$_____")
    else:
        target = get_trigger_arg(bot, triggerargsarray, 1)
        instigator = trigger.nick
        if not target:
            message = instigator + " shows the birdy off to everyone in the room"
        osd(bot, trigger.sender, 'say', "do the thing")
