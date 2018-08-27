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

# author SniperClif


@sopel.module.commands('middle')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    bot.say("\r_________$$____________\n\n"
            "\r________$__$___________\n\n"
            "\r________$__$___________\n\n"
            "\r_______$$__$$__________\n\n"
            "\r______$__$__$_$$_$$____\n\n"
            "\r______$__$__$__$$__$___\n\n"
            "\r_$$$__$__$__$__$$__$___\n\n"
            "\r$___$$_______________$_\n\n"
            "\r$____$$_______________$\n\n"
            "\r_$____________________$\n\n"
            "\r__$___________________$\n\n"
            "\r___$_________________$_\n\n"
            "\r____$_______________$__\n\n"
            "\r_____$_____________$___\n\n"
            "\r______$___________$____\n\n"
            "\r_______$$$$$$$$$$$_____\n\n")
