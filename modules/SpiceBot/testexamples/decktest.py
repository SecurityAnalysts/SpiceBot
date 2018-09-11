#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel import module, tools
import sys
import os
import random
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
# import Spicebucks
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('decktest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'decktest')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, arg):
    myscore = 0
    myhand = get_trigger_arg(bot, arg, '1+') or 'A'
    if len(myhand) >= 12:
        osd(bot, trigger.sender, 'say', "Player wins for having more then 6 cards.")
    else:
        # myhand =get_trigger_arg(bot,myhand,'list')
        osd(bot, trigger.sender, 'say', "Input: " + str(myhand))
        myscore = blackjackscore(bot, myhand)
    osd(bot, trigger.sender, 'say', "Player score is: " + str(myscore))
    reset_database_value(bot, 'casino', 'deckscorecount')


def blackjackscore(bot, hand):
    myscore = 0
    myhand = []

    handlen = len(hand)
    # counter = get_database_value(bot,'casino','deckscorecount')
    #

    for i in range(0, handlen):
        card = get_trigger_arg(bot, hand, i)
        if card.isdigit():
            myscore = myscore+int(card)
        elif(card == 'J' or card == 'Q' or card == 'K'):
            myscore = myscore + 10
        elif card == 'A':
            myscore = myscore + 11
    if myscore > 21:
        # counter = get_database_value(bot,'casino','deckscorecount')
        # if counter >5:
            # return myscore
        if 'A' in hand:
            myhand = hand.replace('A', '1')
            # adjust_database_value(bot, 'casino', 'deckscorecount',1)
            newscore = blackjackscore(bot, myhand)
            return newscore
        else:
            return myscore
    else:
        return myscore


def blackjackreset(bot, player):
    reset_database_value(bot, player, 'myhand')
    reset_database_value(bot, player, 'dealerhand')
    reset_database_value(bot, player, 'mybet')
