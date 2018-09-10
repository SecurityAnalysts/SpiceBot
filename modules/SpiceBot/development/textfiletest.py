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


@sopel.module.commands('count')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    count = txtCount("/home/spicebot/.sopel/SpiceBotdev/modules/SpiceBot/development/test.txt")
    osd(bot, trigger.sender, 'say', str(count))
    test = fileLine("/home/spicebot/.sopel/SpiceBotdev/modules/SpiceBot/development/test.txt", 2)
    osd(bot, trigger.sender, 'say', str(test))
    temp = randomFileLine("/home/spicebot/.sopel/SpiceBotdev/modules/SpiceBot/development/test.txt")
    osd(bot, trigger.sender, 'say', str(temp))


def txtCount(path):
    with open(path) as f:
        line_count = 0
        for line in f:
            line_count += 1

    return line_count


def fileLine(path, number):
    maxLines = txtCount(path)
    if number < 0:
        number = 1
    if number > maxLines:
        number = 1
    file = open(path, "r")
    i = 1
    while i <= number:
        line = file.readline()
        i = i + 1
    return line


def randomFileLine(path):
    maxLines = txtCount(path)
    rand = random.randint(1, maxLines)
    file = open(path, "r")
    i = 1
    while i <= rand:
        line = file.readline()
        i = i + 1
    return line
