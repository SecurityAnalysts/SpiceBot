#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import random
import urllib
import sys
import os
from word2number import w2n
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

fra = 'https://raw.githubusercontent.com/SpiceBot/SpiceBot/master/Text-Files/ferengi_rules.txt'


@sopel.module.commands('ferengi')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    requested = get_trigger_arg(bot, triggerargsarray, 0)
    myline = ''
    if not requested:
        myline = randomfra()
    else:
        requested.lstrip("-")
        if (requested == '0' or requested.lower() == 'zero'):
            myline = 'That doesnt appear to be a rule number.'
        elif requested == 'random':
            myline = randomfra()
        else:
            htmlfile = urllib.urlopen(fra)
            lines = htmlfile.readlines()
            numberoflines = len(lines)

            if requested.isdigit():
                rulenumber = int(requested)
                if rulenumber > numberoflines:
                    myline = "Please select a rule number between 1 and " + str(numberoflines) + ""
                else:
                    myline = get_trigger_arg(bot, lines, rulenumber)
            else:
                try:
                    rulenumber = w2n.word_to_num(str(requested))
                    myline = get_trigger_arg(bot, lines, rulenumber)
                except ValueError:
                    myline = 'That doesnt appear to be a rule number.'
    if not myline or myline == '\n':
        myline = 'There is no cannonized rule tied to this number.'
    osd(bot, trigger.sender, 'say', myline)


# random rule
def randomfra():
    htmlfile = urllib.urlopen(fra)
    lines = htmlfile.read().splitlines()
    myline = random.choice(lines)
    if not myline or myline == '\n':
        myline = randomfra()
    return myline
