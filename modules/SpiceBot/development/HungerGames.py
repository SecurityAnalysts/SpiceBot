#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
from sopel import module, tools
import random
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *
# import Spicebucks

# hungergamesfee=5


@sopel.module.commands('hungergames')
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
    randomtargetarray = []
    botusersarray = get_database_value(bot, bot.nick, 'botusers') or []
    for u in bot.users:
        if u in botusersarray and u != bot.nick:
            randomtargetarray.append(u)
    if randomtargetarray == []:
        osd(bot, trigger.sender, 'say', "There is currently no one available to play the hunger games.")
    else:
        random.shuffle(randomtargetarray)
        totaltributes = len(randomtargetarray)
        if totaltributes == 1:
            osd(bot, trigger.sender, 'say', "There is only one tribute.  Try again later.")
        else:
            osd(bot, trigger.sender, 'say', "Let the Hunger Games begin!  May the odds be ever in your favor.")
            if totaltributes == 2:
                osd(bot, trigger.sender, 'say', "The victor is " + str(randomtargetarray[0]))
            elif totaltributes == 3:
                osd(bot, trigger.sender, 'say', "The first to die was " + str(randomtargetarray[1]) + " The victor is " + str(randomtargetarray[0]))
            else:
                # safetribute = str(randomtargetarray[2])
                # volunteer = str(randomtargetarray[3])
                # randomtargetarray.pop(2)
                # random.shuffle(randomtargetarray)
                # osd(bot, trigger.sender, 'say', volunteer + " volunteered as tribute for " + safetribute + ". The first to die was " + str(randomtargetarray[1]) + ". The victor is " + str(randomtargetarray[0]))
                tributes = []
                weapons = ['dagger', 'sword', 'knife', 'bow and arrow', 'crossbow']
                for tribute in randomtargetarray:
                    random.shuffle(weapons)
                    tributerow = [tribute, 100, weapons[0]]
                    tributes.append(tributerow)
                totaltributes = len(tributes)
                while totaltributes > 1:
                    random.shuffle(tributes)
                    damageone = randint(50, 80)
                    damagetwo = randint(50, 80)
                    if damagetwo == damageone:
                        while damageone == damagetwo:
                            damageone = randint(50, 80)
                            damagetwo = randint(50, 80)
                    osd(bot, trigger.nick, 'priv', tributes[0][0] + " hits " + tributes[1][0] + " with a " + tributes[0][2] + "(-" + str(damageone) + "). " + tributes[1][0] + " hits " + tributes[0][0] + " with a " + tributes[1][2] + "(-" + str(damagetwo) + "). ")
                    tributes[0][1] = tributes[0][1] - damageone
                    tributes[1][1] = tributes[1][1] - damageone
                    if tributes[0][1] <= 0:
                        osd(bot, trigger.nick, 'priv', tributes[1][0] + " killed " + tributes[0][0])
                    if tributes[1][1] <= 0:
                        if len(tributes) > 1:
                            osd(bot, trigger.nick, 'priv', tributes[0][0] + " killed " + tributes[1][0])
                    if tributes[1][1] <= 0:  # remove second tribute first is killed to not mess up order if first is killed
                        tributes.pop(1)
                    if tributes[0][1] <= 0:
                        if len(tributes) > 1:
                            tributes.pop(0)
                    totaltributes = len(tributes)
                # payout =randint(hungergamesfee,35)
                osd(bot, trigger.sender, 'say', "The victor is " + tributes[0][0])
                # Spicebucks.spicebucks(bot,tributes[0][0],'plus',payout)
        # else:
            # osd(bot, trigger.nick, 'priv', "It costs " + str(hungergamesfee) + " to play HungerGames.")
