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


@sopel.module.commands('ich', 'icanhaz')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'ich')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    command = spicemanip(bot, triggerargsarray, '1+')
    if not command:
        command = "Cheezburger"
    rand = random.randint(1,10)
    i = 1
    z = ''
    while i <= rand:
        z = z + 'z'
        i = i + 1
    message = "I can ha" + z + " " + command + "??"
    osd(bot, trigger.sender, 'say', message)
