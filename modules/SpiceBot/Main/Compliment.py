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

compliments = 'https://raw.githubusercontent.com/SpiceBot/SpiceBot/master/Text-Files/compliments.txt'
devcompliments = 'https://raw.githubusercontent.com/SpiceBot/SpiceBot/dev/Text-Files/compliments.txt'
devbot = 'dev'  # Enables the bot to distinguish if in test


@sopel.module.commands('compliment')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    requested = spicemanip(bot, triggerargsarray, 0)
    myline = ''
    if not bot.nick.endswith(devbot):
        filetocheck = compliments  # Master branch
    else:
        filetocheck = devcompliments  # Dev branch
    if not requested:
        myline = randomcompliment(filetocheck)
    else:
        requested.lstrip("-")
        if (requested == '0' or requested.lower() == 'zero'):
            myline = 'That doesnt appear to be a compliment number.'
        elif requested == 'random':
            myline = randomcompliment(filetocheck)
        else:
            htmlfile = urllib.urlopen(filetocheck)
            lines = htmlfile.readlines()
            numberoflines = len(lines)

            if requested.isdigit():
                complimentnumber = int(requested)
                if complimentnumber > numberoflines:
                    myline = "Please select a compliment number between 1 and " + str(numberoflines) + ""
                else:
                    myline = spicemanip(bot, lines, complimentnumber)
            else:
                try:
                    complimentnumber = w2n.word_to_num(str(requested))
                    myline = spicemanip(lines, complimentnumber)
                except ValueError:
                    myline = 'That doesnt appear to be a compliment number.'
    if not myline or myline == '\n':
        myline = 'There is no compliment tied to this number.'
    osd(bot, trigger.sender, 'say', myline)


# work with /me ACTION (does not work with manual weapon)
@module.rule('(?:(feeling|feels).*(sad|upset)).*')  # responds to /me is feeling|feels *** sad|upset
@module.intent('ACTION')
@module.require_chanmsg
def duel_action(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'compliment')
    if not enablestatus:
        execute_reply(bot, trigger, triggerargsarray)


def execute_reply(bot, trigger, triggerargsarray):
    myline = ''
    if not bot.nick.endswith(devbot):
        filetocheck = compliments  # Master branch
    else:
        filetocheck = devcompliments  # Dev branch
    myline = randomcompliment(filetocheck)
    if not myline or myline == '\n':
        myline = 'There is no compliment tied to this number.'
    osd(bot, trigger.sender, 'say', myline)


# random compliment
def randomcompliment(filetocheck):
    htmlfile = urllib.urlopen(filetocheck)
    lines = htmlfile.read().splitlines()
    myline = random.choice(lines)
    if not myline or myline == '\n':
        myline = randomcompliment(filetocheck)
    return myline
