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

fileaddress = 'https://raw.githubusercontent.com/SpiceBot/SpiceBot/master/Text-Files/ferengi_rules.txt'


@sopel.module.commands('getline')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'testline')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Get a line from the given url."""
    linechoice = spicemanip(bot, triggerargsarray, 0) or 'random'
    message = randomurlline(bot, fileaddress)
    osd(bot, trigger.sender, 'say', message)


    # myline = ''
    # if not linechoice:
    #     myline = randomurlline()
    # else:
    #     linechoice.lstrip("-")
    #     if (linechoice == '0' or linechoice.lower() == 'zero'):
    #         myline = 'That doesnt appear to be a rule number.'
    #     elif linechoice == 'random':
    #         myline = randomurlline()
    #     else:
    #         htmlfile = urllib.urlopen(fileaddress)
    #         lines = htmlfile.readlines()
    #         numberoflines = len(lines)
    #
    #         if linechoice.isdigit():
    #             rulenumber = int(linechoice)
    #             if rulenumber > numberoflines:
    #                 myline = "Please select a rule number between 1 and " + str(numberoflines) + ""
    #             else:
    #                 myline = spicemanip(bot, lines, rulenumber)
    #         else:
    #             try:
    #                 rulenumber = w2n.word_to_num(str(linechoice))
    #                 myline = spicemanip(bot, lines, rulenumber)
    #             except ValueError:
    #                 myline = 'That doesnt appear to be a rule number.'
    # if not myline or myline == '\n':
    #     myline = 'There is no cannonized rule tied to this number.'
    # osd(bot, trigger.sender, 'say', myline)


# random rule
def randomurlline(fileurl):
    """Retrieve random line."""
    htmlfile = urllib.urlopen(fileurl)
    lines = htmlfile.read().splitlines()
    myline = random.choice(lines)
    if not myline or myline == '\n':
        myline = randomurlline()
    return myline
